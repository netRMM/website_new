from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from blogs.models import Tag

# Create your models here.
class Category(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name='Category Name', max_length=100, unique=True)
    slug = models.SlugField(verbose_name='slug', null=True, blank=True)
    
    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        value = f'{self.name}'
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
        
        
class Document(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(verbose_name='Title', max_length=100, unique=True)
    content = RichTextUploadingField(verbose_name='Content')
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    slug = models.SlugField(verbose_name='slug', null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='Tags', blank=True)
    category = models.ForeignKey(Category, verbose_name='Document Category', on_delete=models.CASCADE,null=True,blank=True)
    published = models.BooleanField(verbose_name='published', default=False)
    sequence = models.IntegerField(verbose_name='Sequence Number')
    def __str__(self):
        return f'{self.title}'
    
    def save(self, *args, **kwargs):
        value = f'{self.title}'
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)