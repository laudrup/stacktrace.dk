from django.db import models
from django.forms import ModelForm, CharField, Textarea, EmailField, BooleanField,  SlugField
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from imagekit.models import ImageSpec
from imagekit.processors import resize, Adjust
from os import path
import homepage

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
        return path.join('photos', filename)
    else:
        return path.join('photos', instance.gallery.slug, filename)

class Photo(models.Model):
    thumbnail = ImageSpec([Adjust(contrast=1.2, sharpness=1.1),
                           resize.Fit(width=200)], image_field='original_image',
                          format='JPEG', quality=90)
    display_size = ImageSpec([Adjust(contrast=1.2, sharpness=1.1),
                              resize.Fit(width=800, height=600)], image_field='original_image',
                             format='JPEG', quality=90)
    slug = models.SlugField(unique=True, editable=False)
    caption = models.TextField(blank=True)
    gallery = models.ForeignKey('Gallery')
    original_image = models.ImageField(upload_to=get_image_path)

    def __unicode__(self):
        return self.slug

    def next(self):
        next = self.gallery.photo_set.filter(id__gt = self.id)
        if len(next) == 0:
            return None
        return next[0]

    def previous(self):
        prev = self.gallery.photo_set.filter(id__lt = self.id)
        if len(prev) == 0:
            return None
        return prev[0]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.original_image.name)
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
