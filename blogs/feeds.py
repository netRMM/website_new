from django.contrib.syndication.views import Feed
from django.utils.html import escape
from django.urls import reverse
from .models import Article

class LatestArticlesFeed(Feed):
    title = "Latest Articles"
    link = "/blog/rss/"
    description = "Updates on the latest articles posted on the blog."

    def items(self):
        return Article.objects.filter(published=True).order_by('-created_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return escape(item.content)

    def item_author_name(self, item):
        return item.author.get_full_name() if item.author else 'Unknown Author'

    def item_link(self, item):
        return reverse('blogs:article', args=[item.slug])

    def item_pubdate(self, item):
        return item.created_at

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
