from django.contrib import admin
from .models import VisualArt, Category, Post, BlogCategory
from ordered_model.admin import OrderedModelAdmin


# Register your models here.

class VisualArtAdmin(OrderedModelAdmin):
    list_display = ('name', 'move_up_down_links')

admin.site.register(VisualArt, VisualArtAdmin)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(BlogCategory)


