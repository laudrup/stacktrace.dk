from django.db import models

class StackTrace(models.Model):
    trace = models.TextField()

class Post(models.Model):
    pub_date = models.DateTimeField('date published')
    subject = models.CharField(max_length=200)
    body = models.TextField()
