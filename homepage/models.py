from django.db import models
from django.forms import ModelForm, CharField, Textarea, EmailField, BooleanField,  SlugField
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from imagekit.models import ImageSpec
from imagekit.processors import resize, Adjust
from datetime import datetime
import os
import zipfile
import homepage
import Image
import EXIF

class Post(models.Model):
    pub_date = models.DateTimeField('date published')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField(unique=True, editable=False)

    def __unicode__(self):
        return self.subject

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.subject)
        super(Post, self).save(*args, **kwargs)

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    body = models.TextField()
    slug = models.SlugField(unique=True, editable=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateTimeField(auto_now=True, editable=False)
    approved = models.BooleanField(default=True)
    body = models.TextField()

    def __unicode__(self):
        return self.author

class CommentForm(ModelForm):
    author = CharField(label = 'Your name')
    body = CharField(label = 'Comment', widget=Textarea)
    class Meta:
        model = Comment
        exclude = ('post', 'approved')

def get_image_path(instance, filename):
    if instance.gallery is None:
        return os.path.join('photos', filename)
    else:
        return os.path.join('photos', instance.gallery.slug, filename)

class Photo(models.Model):
    thumbnail = ImageSpec([Adjust(contrast=1.2, sharpness=1.1),
                           resize.Fit(width=200)], image_field='image',
                          format='JPEG', quality=90)
    display_size = ImageSpec([Adjust(contrast=1.2, sharpness=1.1),
                              resize.Fit(width=800, height=600)], image_field='image',
                             format='JPEG', quality=90)
    slug = models.SlugField(unique=True, editable=False)
    gallery = models.ForeignKey('Gallery')
    image = models.ImageField(upload_to=get_image_path)
    date_taken = models.DateTimeField(editable=False)

    class Meta:
        ordering = ['date_taken']

    def __unicode__(self):
        return self.slug

    def next(self):
        next = self.gallery.photo_set.filter(date_taken__gt = self.date_taken)
        if len(next) == 0:
            return None
        return next[0]

    def previous(self):
        prev = self.gallery.photo_set.filter(date_taken__lt = self.date_taken)
        if len(prev) == 0:
            return None
        return prev.reverse()[0]

    def download(self):
        return self.image.url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.image.path)
        exif = EXIF.process_file(open(self.image.path, 'rb'))
        exif_date = exif.get('EXIF DateTimeOriginal', None)
        if exif_date is not None:
            d, t = str.split(exif_date.values)
            year, month, day = d.split(':')
            hour, minute, second = t.split(':')
            self.date_taken = datetime(int(year), int(month), int(day),
                                       int(hour), int(minute), int(second))
        else:
            self.date_taken = datetime.now()
        super(Photo, self).save(*args, **kwargs)

    def get_url(self):
        return reverse(homepage.views.photos, args=[self.gallery.slug, self.slug])

class Gallery(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, editable=False)
    date_added = models.DateTimeField(auto_now=True, editable=False)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Gallery, self).save(*args, **kwargs)

    def thumbnail(self):
        photo = self.photo_set.order_by('?')[0]
        return photo.thumbnail

    def get_url(self):
        return reverse(homepage.views.photos, args=[self.slug])

class GalleryUpload(models.Model):
    zip_file = models.FileField(upload_to='temp')
    gallery = models.ForeignKey(Gallery)

    def save(self, *args, **kwargs):
        super(GalleryUpload, self).save(*args, **kwargs)
        gallery = self.process_zipfile()
        super(GalleryUpload, self).delete()
        return gallery

    def process_zipfile(self):
        if os.path.isfile(self.zip_file.path):
            zip = zipfile.ZipFile(self.zip_file.path)
            bad_file = zip.testzip()
            if bad_file:
                raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)
            from cStringIO import StringIO
            for filename in zip.namelist():
                data = zip.read(filename)
                if len(data):
                    # the following is taken from django.newforms.fields.ImageField:
                    #  load() is the only method that can spot a truncated JPEG,
                    #  but it cannot be called sanely after verify()
                    trial_image = Image.open(StringIO(data))
                    trial_image.load()
                    # verify() is the only method that can spot a corrupt PNG,
                    #  but it must be called immediately after the constructor
                    trial_image = Image.open(StringIO(data))
                    trial_image.verify()
                    slug = slugify(os.path.split(filename)[-1])
                    photo = Photo(slug = slug, gallery = self.gallery)
                    photo.image.save(filename, ContentFile(data))
                    self.gallery.photo_set.add(photo)
            zip.close()
            return self.gallery
