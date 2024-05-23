import json

from django.core.files import File
from django.forms import ModelForm, FileField, FileInput, HiddenInput, CharField
from multiupload.fields import MultiFileField, MultiUploadMetaInput

from posts.models import VisualArt
from posts.utils import FirebaseImageUploader, ImageProcessor


class HiddenMultiUploadMetaInput(MultiUploadMetaInput):
    @property
    def is_hidden(self):
        return True


class VisualArtForm(ModelForm):
    ACCEPTED_IMAGE_FILES = [
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/gif",
        "image/webp",
        "image/bmp",
        "image/svg",
        "image/avif",
        ".png",
        ".jpg",
        ".svg",
        ".jpeg",
        ".gif",
        ".webp",
        ".bmp",
        ".avif",
    ]

    # Main Image Upload Field that maps to React components
    main_image_file = FileField(
        required=False,
        label="Main image",
        widget=FileInput(
            attrs={
                "id": "django_main_image_hidden_input",
                "accept": f"{', '.join(ACCEPTED_IMAGE_FILES)}",
            }
        ),
    )
    main_image_deleted = CharField(
        required=False,
        widget=HiddenInput(attrs={"id": "django_main_image_deleted_hidden_input"}),
    )

    additional_images_files = MultiFileField(
        min_num=0,
        max_num=10,
        required=False,
        widget=HiddenMultiUploadMetaInput(
            multiple=True,
            attrs={
                "id": "django_multi_image_hidden_input",
                "style": "display: none;",
                "accept": f"{', '.join(ACCEPTED_IMAGE_FILES)}",
            },
        ),
    )
    already_uploaded_multiple_images = CharField(
        required=False,
        widget=HiddenInput(
            attrs={
                "id": "django_already_uploaded_multi_image_hidden_input",
            },
        ),
    )

    additional_images_deleted = CharField(
        required=False,
        widget=HiddenInput(
            attrs={"id": "django_additional_images_deleted_hidden_input"}
        ),
    )

    def __init__(self, *args, **kwargs):
        self.firebase = FirebaseImageUploader()
        self.image_processor = ImageProcessor()

        super().__init__(*args, **kwargs)

        if self.instance.main_image:
            self.fields["main_image_file"].widget.attrs[
                "initial_value"
            ] = self.instance.main_image

        if additional_images := self.instance.get_additional_images_list():
            self.fields["additional_images_files"].widget.attrs["initial_values"] = (
                json.dumps(additional_images)
            )

    class Meta:
        model = VisualArt
        fields = [
            "name",
            "description",
            "show",
            "categories",
            "likes",
        ]

    def save(self, commit=True, *args, **kwargs):
        instance: VisualArt = super().save(commit=False)

        self.handle_upload_main_image(instance)
        self.handle_upload_additional_images(instance)

        if commit:
            instance.save()
        return instance

    def handle_upload_main_image(self, instance: VisualArt):
        if main_image_file := self.cleaned_data["main_image_file"]:

            # Vercel 413 File limit size
            main_image_file = self.limit_image_size(main_image_file)

            instance.main_image = self.firebase.upload_image(main_image_file)

            thumbnail = self.image_processor.make_thumbnail_of_file(main_image_file)
            instance.thumbnail = self.firebase.upload_image(thumbnail)
        else:
            if self.cleaned_data["main_image_deleted"] == "true":
                instance.main_image = ""
                instance.thumbnail = ""

    def handle_upload_additional_images(self, instance: VisualArt):
        already_uploaded_multiple_images = json.loads(
            self.cleaned_data["already_uploaded_multiple_images"]
        )
        already_uploaded_multiple_images_names = [
            image["name"] for image in already_uploaded_multiple_images
        ]

        if images_deleted := json.loads(self.cleaned_data["additional_images_deleted"]):
            already_uploaded_multiple_images = [
                image
                for image in already_uploaded_multiple_images
                if image["name"] not in images_deleted
            ]

        additional_images = []
        if files := self.cleaned_data["additional_images_files"]:
            for file in files:
                if file.name in already_uploaded_multiple_images_names:
                    continue

                additional_images.append(
                    {"name": file.name, "url": self.firebase.upload_image(file)}
                )

        instance.additional_images = json.dumps(
            [*additional_images, *already_uploaded_multiple_images]
        )

    def limit_image_size(self, image_file: File) -> File:
        # If larger than 4.5 mbs (Vercel 413: FUNCTION_PAYLOAD_TOO_LARGE)
        if (image_file.size // 1024**2) >= 4.5:
            return self.image_processor.make_thumbnail_of_file(
                image_file,
                new_size=(1024, 1024),
            )
        else:
            return image_file
