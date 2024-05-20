from django.forms import ModelForm, FileField, FileInput
from django.core.files import File

from posts.models import VisualArt
from posts.utils import FirebaseImageUploader, ImageProcessor


class VisualArtForm(ModelForm):
    art = FileField(widget=FileInput())

    def __init__(self, *args, **kwargs):
        self.firebase = FirebaseImageUploader()
        super().__init__(*args, **kwargs)

    class Meta:
        model = VisualArt
        fields = [
            "name",
            "art",
            "description",
            "show",
            "categories",
            "likes",
        ]

    def save(self, commit=True, *args, **kwargs):
        instance: VisualArt = super().save(commit=False)

        self.handle_art_upload(instance)

        if commit:
            instance.save()
        return instance

    def handle_art_upload(self, instance: VisualArt):
        art_image = self.cleaned_data.get("art", None)
        if art_image and isinstance(art_image, File):
            instance.art = self.firebase.upload_image(art_image)

            thumbnail = ImageProcessor().make_thumbnail(art_image)
            instance.thumbnail = self.firebase.upload_image(thumbnail)
