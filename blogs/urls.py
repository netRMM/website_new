from django.urls import path, include
from . import views
from .feeds import LatestArticlesFeed

app_name = 'blogs'

urlpatterns= [

    # Blogs
    path('', views.blog, name='blog'),
    path('category/<slug>/', views.blog_category, name='blog_category'),

    # Individual Article
    path('<slug>', views.article, name='article'),

    # RSS Feed
    path('rss/', LatestArticlesFeed(), name='article_feed'),
]
