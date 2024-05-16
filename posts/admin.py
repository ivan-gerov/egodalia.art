from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin

from posts.models import AboutMe, VisualArt, Category, Post, BlogCategory
from posts.forms import VisualArtForm


# Register your models here.


class VisualArtAdmin(OrderedModelAdmin):
    form = VisualArtForm
    list_display = ("name", "move_up_down_links")


admin.site.register(VisualArt, VisualArtAdmin)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(BlogCategory)
admin.site.register(AboutMe)
