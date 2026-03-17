from http.client import HTTPResponse
from django.shortcuts import render
from .models import Article, Tag, Category
# Pagination
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404


# Create your views here.

def blog_category(request,slug):
    try:
        category = Category.objects.get(slug=slug)
        articles = Article.objects.filter(published=True,category=category).order_by('-created_at')
    except Category.DoesNotExist:
        category = None
        articles = Article.objects.none()
    paginator = Paginator(articles, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    tags = Tag.objects.all()
    categories = Category.objects.all()

    context = {
        "category":category,
        'articles': articles,
        'tags': tags,
        'categories': categories
    }
    return render(request, 'blogs/blog.html', context)


def blog(request):
    if 'tag' in request.GET:
        try:
            tag = Tag.objects.get(slug=request.GET.get('tag'))
            articles = Article.objects.filter(published=True, tags__slug__in=[tag.slug]).order_by('-created_at')
        except:
            tag = None
            articles = Article.objects.filter(published=True).order_by('-created_at')
    else:
        tag = None
        articles = Article.objects.filter(published=True).order_by('-created_at')
    tags = Tag.objects.all()
    paginator = Paginator(articles, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    categories = Category.objects.all()

    context = {
        'page_name':'blogs',
        'articles': articles,
        'tag': tag,
        'tags': tags,
        'categories':categories
    }
    return render(request, 'blogs/blog.html', context)



def article(request, slug):
    try:
        article = Article.objects.get(slug=slug, published=True)
    except:
        article = None
    tags = Tag.objects.all()
    categories = Category.objects.all()

    context = {
        'article': article,
        'tags': tags,
        'categories':categories
    }
    return render(request, 'blogs/article.html', context)
