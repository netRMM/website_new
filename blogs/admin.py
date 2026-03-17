from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Tag, Category, MetaTags

# Register your models here.
@admin.action(description='Publish selected')
def make_published(modeladmin, request, queryset):
    queryset.update(published=True)


@admin.action(description='Unpublish selected')
def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'title', 'created_at', 'published', 'link',)

    actions = [make_unpublished, make_published,]

    search_fields = ('title',)

    list_filter = [
        'published',
    ]

    list_per_page = 10

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

    def image_tag(self, obj):
        return format_html(f'<img src="{obj.banner.url}" style="height:10vh; border-radius: 5%;" />')

    def link(self, obj):
        return format_html(f'<a href="{obj.url()}" target="_blank">Visit</a>')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at',)

    search_fields = ('name',)

    list_per_page = 10

    # def link(self, obj):
    #     return format_html(f'<a href="{obj.url()}" target="_blank">Visit</a>')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

@admin.register(MetaTags)
class MetaTagsAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'banner', 'description', 'keywords', 'follow', 'index', 'author')