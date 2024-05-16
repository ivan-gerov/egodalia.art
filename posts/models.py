from ordered_model.models import OrderedModel
from django.db import models
from django_limits.limiter import Limiter

# Create your models here


class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.name + ", ID: " + str(self.id)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "categories"
        verbose_name = "category"


class VisualArt(OrderedModel):
    name = models.CharField(max_length=100)
    art = models.TextField()
    thumbnail = models.TextField(blank=True, default=None)
    description = models.TextField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    show = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category)
    likes = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "arts"
        verbose_name = "art"

    def __str__(self):
        return self.name

    def admin_image(self):
        return self.art


class Comment(models.Model):
    posted_by = models.CharField(max_length=32)
    comment = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    visualart = models.ForeignKey(VisualArt, on_delete=models.CASCADE)


class BlogCategory(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.name + ", ID: " + str(self.id)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "blog categories"
        verbose_name = "blog category"


class Post(models.Model):
    title = models.CharField(max_length=80)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    category = models.ForeignKey(
        BlogCategory,
        verbose_name="Category",
        on_delete=models.PROTECT,
        null=True,
        default=None,
    )
    views = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class AboutMe(
    models.Model
):  # this is a de-facto model for simplicity - doesn't have to be a model, I was just lazy and this is the easiest way
    title = models.CharField(max_length=80)
    body = models.TextField()

    def __str__(self):
        return "About Me: %s" % self.title

    class Meta:
        verbose_name_plural = "About Me"  # no plural
        verbose_name = "About Me"


class MyLimiter(Limiter):
    rules = {
        AboutMe: [
            {
                "limit": 1,
                "message": "Only one About Me allowed!",
            },
        ]
    }
