from django.db import models

# Create your models here


class VisualArt(models.Model):
    name = models.CharField(max_length=100)
    art = models.ImageField(upload_to = 'art/')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    show = models.BooleanField(default = True)

    def __str__(self):
        return 'Art: ' + self.name

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "arts"
        verbose_name = "art"
