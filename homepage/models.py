from django.db import models
from django.forms import ModelForm, CharField, Textarea, EmailField, BooleanField, DateTimeField, SlugField
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from imagekit.models import ImageSpec
from imagekit.processors import resize, Adjust
import homepage

class Post(models.Model):
    pub_date = models.DateTimeField('date published')
    subject = models.CharField(max_length=200)
    body = models.TextField()

    def __unicode__(self):
        return self.subject

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    body = models.TextField()

    def __unicode__(self):
        return self.name

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

class Photo(models.Model):
    original_image = models.ImageField(upload_to='photos')
    thumbnail = ImageSpec([Adjust(contrast=1.2, sharpness=1.1),
                           resize.Fit(width=200)], image_field='original_image',
                          format='JPEG', quality=90)
    title = models.CharField(max_length=100, unique=True)
    title_slug = models.SlugField(unique=True, editable=False)
    caption = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
        super(Photo, self).save(*args, **kwargs)

    def get_url(self):
        return self.original_image.url

class Gallery(models.Model):
    title = models.CharField(max_length=100)
    title_slug = models.SlugField(unique=True, editable=False)
    date_added = models.DateTimeField(auto_now=True, editable=False)
    description = models.TextField(blank=True)
    photos = models.ManyToManyField('Photo', related_name='galleries', null=True, blank=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
        super(Gallery, self).save(*args, **kwargs)

    def thumbnail(self):
        photo = self.photos.order_by('?')[0]
        return photo.thumbnail

    def get_url(self):
        return reverse(homepage.views.photos, args=[self.title_slug])
