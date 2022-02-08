from django.shortcuts import render
from .models import VisualArt
from django.http import HttpResponse

# Create your views here.

def getVisualArt(request, artID):
    print(request.path)
    try:
        artObj = VisualArt.objects.get(id=artID)
        if request.user.is_superuser:
            show = True
        else:
            show = artObj.show
    except:
        show = False
    if not show:
        return HttpResponse("Art not found", status=404)
    image_data = open(artObj.art.path, 'rb').read()
    return HttpResponse(image_data, content_type='image/png')
