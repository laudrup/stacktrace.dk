from django.db import models
from django.forms import ModelForm, CharField, Textarea, EmailField, BooleanField, SlugField
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.conf import settings
from datetime import datetime
from thumbs import ImageWithThumbsField
import os
import zipfile
import homepage
import Image
import pyexiv2

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
    slug = models.SlugField(unique=True, editable=False)
    gallery = models.ForeignKey('Gallery')
    image = ImageWithThumbsField(upload_to=get_image_path, sizes=((200,150),(800,600)))
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
        metadata = pyexiv2.ImageMetadata(self.image.path)
        metadata.read()
        if 'Exif.DateTimeOriginal' in metadata:
            self.date_taken = metadata['Exif.DateTimeOriginal'].value
        elif 'Exif.Image.DateTime' in metadata:
            self.date_taken = metadata['Exif.Image.DateTime'].value
        else:
            self.date_taken = datetime.now()
        super(Photo, self).save(*args, **kwargs)
        self.gallery.update_dates()

def get_zipfile_path(instance, filename):
    return os.path.join('photos', instance.slug, filename)

class Gallery(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, editable=False)
    date_added = models.DateTimeField(auto_now=True, editable=False)
    description = models.TextField(blank=True)
    first_photo_date = models.DateTimeField(editable=False, null=True)
    last_photo_date = models.DateTimeField(editable=False, null=True)
    zip_file = models.FileField(editable=False, null=True, upload_to=get_zipfile_path)

    class Meta:
        ordering = ['-first_photo_date']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Gallery, self).save(*args, **kwargs)

    # XXX: Rename to example, random_image or something
    def thumbnail(self):
        photos = self.photo_set.order_by('?')
        if len(photos) is 0:
            return None
        return photos[0].image

    # XXX: Change to update() or even better, react to a signal or something...
    def update_dates(self):
        first_photo = self.photo_set.all()[0]
        last_photo = self.photo_set.all().reverse()[0]
        self.first_photo_date = first_photo.date_taken
        self.last_photo_date = last_photo.date_taken
        if self.zip_file:
            self.zip_file.delete()
        super(Gallery, self).save()

    def create_zipfile(self):
        tmpname = os.path.join(settings.MEDIA_ROOT, 'temp', self.slug + '.zip')
        zip = zipfile.ZipFile(tmpname, 'w')
        for photo in self.photo_set.all():
            zip.write(photo.image.path, os.path.split(photo.image.path)[-1])
        zip.close()
        self.zip_file.save(self.slug + '.zip', ContentFile(open(tmpname).read()))

    def zip_url(self):
        if not self.zip_file:
            self.create_zipfile()
        return self.zip_file.url

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
