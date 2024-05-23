from django.shortcuts import render, redirect
from .models import AboutMe, Category, VisualArt, Post, BlogCategory
from django.http import HttpResponse
from ratelimit.decorators import ratelimit
from markdown import Markdown


markdowner = Markdown()


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
    print(artObj.art.url)
    return redirect(artObj.art.url)


def getThumbnail(request, artID):
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
    return redirect(artObj.thumbnail.url)


def index(request):
    categories = Category.objects.filter(show=True)
    arts = VisualArt.objects.filter(show=True).order_by("-created_at")
    content = {"categories": categories, "arts": arts, "isIndex": True}
    return render(request, "posts/index.html", content)


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
    categories = Category.objects.filter(show=True)
    if artObj.description is not None:
        artObj.description = markdowner.convert(artObj.description)
    else:
        artObj.description = ""
    content = {
        "categories": categories,
        "art": artObj,
        "isIndex": True,
        "additional_images": artObj.get_additional_images_urls(),
    }
    return render(request, "posts/art_page.html", content)


def getArtsFromCategory(request, categoryID):
    categories = Category.objects.filter(show=True)
    arts = VisualArt.objects.filter(show=True, categories__in=categoryID)
    content = {"categories": categories, "arts": arts, "categoryID": int(categoryID)}
    return render(request, "posts/index.html", content)


def getBlogHome(request):
    blogPosts = Post.objects.all()
    for post in blogPosts:
        post.body = markdowner.convert(post.body)

    categories = BlogCategory.objects.all()
    headPost = blogPosts[0]
    blogPosts = blogPosts[1:]
    content = {
        "posts": blogPosts,
        "headPost": headPost,
        "blog_categories": categories,
        "isBlog": True,
    }
    return render(request, "posts/blog_home.html", content)


def getBlogPost(request, postID):
    try:
        post = Post.objects.get(id=postID)
    except:
        return HttpResponse("Post not found", status=404)
    categories = BlogCategory.objects.all()

    post.body = markdowner.convert(post.body)
    content = {"blog_categories": categories, "post": post, "isBlog": True}
    return render(request, "posts/blog_post.html", content)


def getPostsFromCategory(request, categoryID):
    try:
        category = BlogCategory.objects.get(id=categoryID)
    except:
        return HttpResponse("Post not found", status=404)
    posts = Post.objects.filter(category=category)
    for post in posts:
        post.body = markdowner.convert(post.body)
    categories = BlogCategory.objects.all()
    content = {"posts": posts, "blog_categories": categories, "isBlog": True}
    return render(request, "posts/blog_categorypage.html", content)


def getMe(request):
    aboutMe = AboutMe.objects.all()[0]
    if aboutMe.body is not None:
        aboutMe.body = markdowner.convert(aboutMe.body)
    content = {"isAboutMe": True, "aboutMe": aboutMe}
    return render(request, "posts/me.html", content)
