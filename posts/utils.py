import typing
import io
import mimetypes

from PIL import Image
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from firebase_admin import storage


class FirebaseImageUploader:
    def __init__(self):
        self.storage = storage.bucket(name=settings.FIREBASE_BUCKET)

    def upload_image(self, image: File) -> str:
        return self.upload_file(file_contents=image, file_name=image.name)

    def upload_file(
        self,
        file_contents: typing.Union[io.BytesIO, File],
        file_name: str,
    ) -> str:
        storage_blob = self.storage.blob(blob_name=file_name)
        storage_blob.upload_from_file(file_contents)
        storage_blob.make_public()
        return storage_blob.public_url


class ImageProcessor:
    def convert_file_to_image(self, file: File) -> Image.Image:
        return Image.open(file.file)

    def convert_image_to_file(self, image: Image.Image, filename: str) -> File:
        thumbnail_buffer = io.BytesIO()
        image.save(thumbnail_buffer, format="JPEG")
        thumbnail_buffer.seek(0)
        # Create an InMemoryUploadedFile from the BytesIO buffer
        file_content = thumbnail_buffer.getvalue()
        content_file = ContentFile(file_content, name=filename)

        # Determine the content type based on the filename extension
        content_type, _ = mimetypes.guess_type(filename)
        content_type = content_type or "application/octet-stream"

        # Create and return the InMemoryUploadedFile instance
        return InMemoryUploadedFile(
            file=content_file,
            field_name=None,
            name=filename,
            content_type=content_type,
            size=len(file_content),
            charset=None,
        )

    def make_thumbnail_of_file(
        self, file: File, new_size: typing.Optional[tuple] = None
    ) -> File:
        if not new_size:
            new_size = (1200, 1200)

        image = self.convert_file_to_image(file)
        image.thumbnail(new_size)
        return self.convert_image_to_file(
            image,
            filename=f"thumnail.{file.name}",
        )
