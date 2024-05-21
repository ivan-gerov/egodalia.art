from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html

from ordered_model.admin import OrderedModelAdmin

from posts.models import AboutMe, VisualArt, Category, Post, BlogCategory
from posts.forms import VisualArtForm


# Register your models here.


class VisualArtAdmin(OrderedModelAdmin):
    form = VisualArtForm
    list_display = (
        "get_main_image_display",
        "name",
        "move_up_down_links",
        "created_at",
    )
    actions = ("hide_artwork", "show_artwork")

    @admin.action(description="Hide selected artwork")
    def hide_artwork(modeladmin, request, queryset):
        queryset.update(show=False)

    @admin.action(description="Show selected artwork")
    def show_artwork(modeladmin, request, queryset):
        queryset.update(show=True)

    def get_main_image_display(self, obj: VisualArt):
        if obj.thumbnail:
            return format_html(
                f'<img src="{obj.thumbnail}" style="max-width:200px; max-height:200px"/>'
            )
        else:
            default_art_image_url = static("posts/art_placeholder.svg")
            return format_html(
                f'<img src="{default_art_image_url}"'
                ' style="max-width:200px; max-height:200px"/>'
            )

    get_main_image_display.allow_tags = True
    get_main_image_display.short_description = "Main image"


admin.site.register(VisualArt, VisualArtAdmin)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(BlogCategory)
admin.site.register(AboutMe)
