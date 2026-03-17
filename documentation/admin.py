from django.contrib import admin
from .models import *
# Register your models here.

@admin.action(description='Publish selected')
def make_published(modeladmin, request, queryset):
    queryset.update(published=True)


@admin.action(description='Unpublish selected')
def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('unique_id','name','slug')
    
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title','created_at','slug','category','published')
    actions = [make_unpublished, make_published,]

    search_fields = ('title',)

    list_filter = [
        'published',
    ]

    list_per_page = 10    