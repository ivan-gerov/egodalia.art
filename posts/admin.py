from django.contrib import admin
from .models import VisualArt, Category, Post, BlogCategory

# Register your models here.

admin.site.register(VisualArt)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(BlogCategory)


