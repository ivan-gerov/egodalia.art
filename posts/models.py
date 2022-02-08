from django.db import models
from django.contrib import admin
import os
# Create your models here

class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name + ', ID: ' + str(self.id)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "categories"
        verbose_name = "category"

def content_file_name_art(instance, filename):
    print(instance)
    print(instance.pk)
    ext = filename.split('.')[-1]
    filename = "{}.{}".format(instance.id, ext)
    return os.path.join('art', filename)

class VisualArt(models.Model):
    name = models.CharField(max_length=100)
    art = models.ImageField(upload_to = 'art/')
    description = models.TextField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    show = models.BooleanField(default = True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    def admin_image(self):
        return '<a href="/art/{}">art/{}</a>'.format(self.id) 



    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "arts"
        verbose_name = "art"

