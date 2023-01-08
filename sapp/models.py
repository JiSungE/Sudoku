from django.db import models

# Create your models here.

class Post(models.Model):
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    text = models.TextField()

class Ranking(models.Model):
    name = models.CharField(max_length=255)
    elapsed_time = models.TimeField()