from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(ReleaseYear)
class ReleaseYearAdmin(admin.ModelAdmin):
    list_display = ('year',)

@admin.register(ReleaseNote)
class ReleaseYearAdmin(admin.ModelAdmin):
    list_display = ('title','body','month','version','year')