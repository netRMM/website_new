from urllib.parse import urlparse, urlunparse, urljoin
from .models import MetaTags

def meta_tags(request):
    meta_title = None
    meta_description = None
    meta_keywords = None
    meta_robots = None
    meta_canonical = None
    meta_author = None
    banner = None

    parsed_url = urlparse(request.build_absolute_uri())
    url_path = urlunparse(('', '', parsed_url.path, '', "", ''))

    try:
        meta_tag = MetaTags.objects.get(url=url_path)
        
        if meta_tag.title:
            meta_title = meta_tag.title
        if meta_tag.description:
            meta_description = meta_tag.description
        if meta_tag.keywords:
            meta_keywords = meta_tag.keywords

        meta_robots = ""
        if meta_tag.index:
            meta_robots += "index"
        else:
            meta_robots += "noindex"

        if meta_tag.follow:
            meta_robots += ", follow"
        else:
            meta_robots += ", nofollow"

        
        if meta_tag.author:
            meta_author = meta_tag.author
        if meta_tag.banner:
            banner = urljoin(request.build_absolute_uri('/'), meta_tag.banner)

        

    except MetaTags.DoesNotExist:
        pass

    return {
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'meta_robots': meta_robots,
        'meta_canonical': meta_canonical,
        'meta_author': meta_author,
        'banner': banner,
    }
