from django.shortcuts import render
from .models import Category, VisualArt
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


def index(request):
    categories = Category.objects.filter(show=True)
    arts = VisualArt.objects.filter(show=True)
    content = {
        'categories': categories,
        'arts': arts,
        'isIndex': True
    }
    return render(request, 'posts/index.html', content)

def art(request, artID):
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
    return HttpResponse(artID)

def getArtsFromCategory(request, categoryID):
    categories = Category.objects.filter(show=True)
    arts = VisualArt.objects.filter(show=True, categories__in=categoryID)
    content = {
        'categories': categories,
        'arts': arts,
        'categoryID': int(categoryID)
    }
    return render(request, 'posts/index.html', content)
