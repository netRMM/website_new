from django.contrib import admin
from .models import Global

# Register your models here.
@admin.register(Global)
class GlobalAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'description',)

# Register your models here.
