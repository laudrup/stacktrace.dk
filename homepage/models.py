from django.db import models

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
    date = models.DateTimeField()
    spam = models.CharField(max_length=1, blank=True)
    body = models.TextField()

    def __unicode__(self):
        return self.author
