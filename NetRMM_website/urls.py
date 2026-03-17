"""NetRMM_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .sitemaps import (
    StaticViewSitemap,
    DocsDetailSitemap,
    ArticleSitemap,
    ReleaseNoteDetailSitemap,
)

sitemaps = {

    'static': StaticViewSitemap,
    'docs_details': DocsDetailSitemap,
    'articles': ArticleSitemap,
    'release_notes': ReleaseNoteDetailSitemap,
}

admin.site.site_header = "NetRMM Website Admin"
admin.site.site_title = "NetRMM Website Admin Portal"
admin.site.index_title = "Welcome to NetRMM Website Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('',include('customers.urls')),
    
    # Login
    path('request-login/',views.login,name='login'),
    # Feature Request
    path('featurerequest/', views.featurerequest, name='featurerequest'),
    # Pricing
    path('pricing/', views.pricing, name='pricing'),
    # Build With Us
    path('buildwithnetrmm/', views.buildwithnetrmm, name='buildwithnetrmm'),
    # Features
    path('features/', views.features, name='features'),
    # FAQ
    path('netrmm-faqs/', views.faqs, name='faq'),
    # Security
    path('security/', views.security, name='security'),
    # Terms of Service
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    # Privacy Policy
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    #Careers
    path('careers/', views.careers, name='careers'),
    # About
    path('about/', views.about, name='about'),
    # Blog
    path('blog/', include('blogs.urls')),
    # Docs
    path('docs/', include('documentation.urls')),
    # Ckeditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # Release Notes
    path('',include('releasenote.urls')),

    # APIS 
    path('api/customers/',include('customers.apis.urls','customers_api')),
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
