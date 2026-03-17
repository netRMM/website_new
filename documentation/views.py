from django.shortcuts import render
from blogs.models import Tag
from .models import *

# Create your views here.
def all_docs(request):
    categories = Category.objects.all()
    documents = Document.objects.filter(published=True)
    tags = Tag.objects.all()
    if 'tag' in request.GET:
        try:
            tag = Tag.objects.get(slug=request.GET.get('tag'))
            documents = Document.objects.filter(published=True, tags__slug__in=[tag.slug]).order_by('-created_at')
        except:
            tag = None
            documents = Document.objects.filter(published=True).order_by('-created_at')
    elif 'category' in request.GET:
        try:
            documents = Document.objects.filter(published=True, category__slug=request.GET.get('category')).order_by('-created_at')
        except:
            documents = Document.objects.filter(published=True).order_by('-created_at')
            
    else:
        tag = None
        documents = Document.objects.filter(published=True).order_by('-created_at')
    context = {
        'categories':categories,
        'page_name':'Docs',
        'documents':documents,
        'tags': tags
    }
    return render(request,'docs/all_docs.html',context)

def document_view(request,cat,doc):
    if cat == '-':
        document = Document.objects.get(slug=doc)
    else:
        document = Document.objects.get(slug=doc,category__slug=cat)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    context = {
        'categories':categories,
        'document':document,
        'title':document.title,
        'tags': tags
    }
    return render(request,'docs/document.html',context)