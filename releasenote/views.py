from django.shortcuts import render
from .models import ReleaseNote
from django.core.paginator import Paginator

# Create your views here.

def releasenotes(request):
    if 'version' in request.GET:
        if request.GET.get('version') != '':
            try:
                releases = ReleaseNote.objects.filter(version=request.GET.get('version')).order_by('-version')
            except:
                releases = ReleaseNote.objects.all().order_by('-version')
        else:
            releases = ReleaseNote.objects.all().order_by('-version')
    else:
        releases = ReleaseNote.objects.all().order_by('-version')
    paginator = Paginator(releases, 10)
    page = request.GET.get('page')
    releases = paginator.get_page(page)
    context = {
        'page_name': 'Release Notes',
        'releases':releases
    }
    return render(request, 'release_notes/release_notes.html', context)


def releasenote_detailed(request,release_id):
    releases = ReleaseNote.objects.get(unique_id=release_id)
    context = {
        'title':releases.title,
        'release':releases
    }
    return render(request, 'release_notes/releasenote_detailed.html', context)