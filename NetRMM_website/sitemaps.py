# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from releasenote.models import ReleaseNote
from documentation.models import Document, Category
from blogs.models import Article, Tag

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 1.0

    def items(self):
        return [
            'homepage',
            'login',
            'featurerequest',
            'pricing',
            'buildwithnetrmm',
            'features',
            'faq',
            'security',
            'terms_of_service',
            'privacy_policy',
            'careers',
            'about',
            'releasenote:releasenotes',
            'docs:all_docs',
            'blogs:blog', 
            'blogs:article_feed',
            'customers:contact_us', 
            'customers:add_customer',
        ]

    def location(self, item):
        return reverse(item)

class DocsDetailSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Document.objects.filter(published=True).order_by('-created_at')

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('docs:document_view', args=[obj.category.slug if obj.category else '-', obj.slug])

class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return Article.objects.filter(published=True).order_by('-created_at')

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return obj.url()

class ReleaseNoteDetailSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ReleaseNote.objects.all()

    def lastmod(self, obj):
        return obj.year.year

    def location(self, obj):
        return reverse('releasenote:releasenote_detailed', args=[str(obj.unique_id)])

