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
    def make_thumbnail(self, art_image: File) -> InMemoryUploadedFile:
        image = Image.open(art_image.file)
        MAX_SIZE = (1200, 1200)
        image.thumbnail(MAX_SIZE)

        thumbnail_buffer = io.BytesIO()
        image.save(thumbnail_buffer, format="JPEG")
        thumbnail_buffer.seek(0)

        return self.create_inmemory_uploaded_file(
            thumbnail_buffer,
            filename=f"thumnail.{art_image.name}",
        )

    def create_inmemory_uploaded_file(
        self, file_buffer: io.BytesIO, filename: str
    ) -> InMemoryUploadedFile:
        # Create an InMemoryUploadedFile from the BytesIO buffer
        file_content = file_buffer.getvalue()
        content_file = ContentFile(file_content, name=filename)

        # Determine the content type based on the filename extension
        content_type, _ = mimetypes.guess_type(filename)
        content_type = content_type or "application/octet-stream"

        # Create and return the InMemoryUploadedFile instance
        uploaded_file = InMemoryUploadedFile(
            file=content_file,
            field_name=None,
            name=filename,
            content_type=content_type,
            size=len(file_content),
            charset=None,
        )

        return uploaded_file
