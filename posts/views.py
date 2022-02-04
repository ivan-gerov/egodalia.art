from django.shortcuts import render
from .models import VisualArt
from django.http import HttpResponse

# Create your views here.

def getVisualArt(request, artID):
    try:
        artObj = VisualArt.objects.get(id=artID)
        show = artObj.show
    except:
        show = False
    if not show:
        return HttpResponse("Art not found", status=404)
    image_data = open(artObj.art.path, 'rb').read()
    return HttpResponse(image_data, content_type='image/png')
