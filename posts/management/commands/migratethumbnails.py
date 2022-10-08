from posts.models import VisualArt
from django.core.management.base import BaseCommand, CommandError

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'Creates thumbnails for all the arts that don\'t have one'

    def handle(self, *args, **options):
        for instance in VisualArt.objects.all():
            if instance.thumbnail.name == None:         
                try:
                    f = BytesIO()
                    image = Image.open(instance.art.path) 
                    MAX_SIZE = (1200, 1200)
                    image.thumbnail(MAX_SIZE)

                    ext = instance.art.name.split('.')[-1]
                    if ext in ['jpg', 'jpeg']:
                        ftype = 'JPEG'
                    elif ext == 'gif':
                        ftype = 'GIF'
                    elif ext == 'png':
                        ftype = 'PNG'
                    else:
                        return False
                    image.save(f, format=ftype)
                    s = f.getvalue()
                    instance.thumbnail.save(instance.art.name, ContentFile(s))
                    print("Successful thumbnail creation for art with id", instance.id)
                except Exception as e:
                    print("[*] Something went wrong")
                    print(e)
                finally:
                    f.close()

