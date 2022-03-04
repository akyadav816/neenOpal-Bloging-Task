from django.db import models

# Create your models here.

class Post_blog(models.Model):
    title = models.CharField(max_length=20)
    created_Date = models.DateField()
    owner = models.CharField(max_length=20)
    desc = models.TextField()
    is_Published = models.CharField(max_length=10)