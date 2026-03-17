from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid
from django.urls import reverse
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
import os

def validate_image(image):
    file_size = image.file.size
    limit_kb = 512
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)

class Category(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name='Name', max_length=100, unique=True)
    description = models.CharField(max_length=160,verbose_name='Short Description',null=True)
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    slug = models.SlugField(verbose_name='slug', null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('blogs:blog_category', kwargs={'slug': self.slug})
        

    def save(self, *args, **kwargs):
        if not self._state.adding:
            existing_category = Category.objects.get(unique_id=self.unique_id)
            # Check if the name has changed
            if existing_category.name != self.name:
                # Delete the existing MetaTags entry
                MetaTags.objects.filter(url=existing_category.get_absolute_url()).delete()
        
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

        url = self.get_absolute_url()
        defaults = {
            'title': self.name,
            'description': self.description,
            'keywords': '',  
            'follow': True,
            'index': True,
            
        }
        MetaTags.objects.update_or_create(url=url, defaults=defaults)

    def delete(self, *args, **kwargs):
        print("checking delete method of models")
        MetaTags.objects.filter(url=self.get_absolute_url()).delete()
        super().delete(*args, **kwargs)
    
class MetaTags(models.Model):
    url = models.TextField(verbose_name="Relative URL", null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name="Meta Title", null=True, blank=True)
    banner = models.URLField(max_length=255, verbose_name="Banner URL", null=True, blank=True)
    description = models.TextField(verbose_name="Meta Description", null=True, blank=True)
    keywords = models.TextField(verbose_name="Meta Keywords", null=True, blank=True)
    follow = models.BooleanField(default=True, verbose_name="Follow Links")
    index = models.BooleanField(default=True, verbose_name="Index Page")
    author = models.CharField(max_length=255, verbose_name="Meta Author", null=True, blank=True)

# Create your models here.
class Article(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(verbose_name='Title', max_length=70, unique=True)
    description = models.CharField(max_length=160,verbose_name='Short Description',null=True)
    content = models.TextField(verbose_name='Content')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    banner = models.ImageField(verbose_name='Banner',upload_to='banners/blogs', default='defaults/blog_default.webp', validators=[validate_image])
    created_at = models.DateTimeField(verbose_name='Created At', auto_now_add=True,null=True)
    updated_at = models.DateTimeField(verbose_name='Updated At', auto_now=True)
    pub_date = models.DateTimeField(default=None,verbose_name='Publish Date', null=True, blank=True)
    published = models.BooleanField(verbose_name='published', default=False)
    slug = models.SlugField(verbose_name='slug', null=True, blank=True)
    tags = models.ManyToManyField('Tag', verbose_name='Tags', blank=True)

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        ordering = ['-pub_date']
        
    
    def clean(self):
        super().clean()
        if self.description and len(self.description) < 50:
            raise ValidationError({'description': 'The short description must be at least 50 characters long.'})

    def url(self):
        self.link = reverse('blogs:article',  kwargs={'slug':self.slug})
        return self.link

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        
        if self._state.adding:
            if self.published:
                self.pub_date = self.updated_at
            else:
                self.pub_date = None
        else:
            this = Article.objects.get(unique_id=self.unique_id)
            if this.published != self.published:
                if self.published:
                    self.pub_date = self.updated_at
                else:
                    self.pub_date = None
            if this.title != self.title:
                # Delete the existing MetaTags entry
                MetaTags.objects.filter(url=this.url()).delete()

        try:
            this = Article.objects.get(id=self.id)
            if this.banner != self.banner:
                if os.path.isfile(this.banner.path) and self.banner.path != 'defaults/blog_default.webp':
                    os.remove(this.banner.path)
        except Article.DoesNotExist:
            pass
        super().save(*args, **kwargs)  
        

        # URL for the MetaTags entry
        url = self.url()

        defaults = {
            'url': url,
            'title': self.title,
            'description': self.description,
            'keywords': ', '.join(tag.name for tag in self.tags.all()),
            'follow': True,  
            'index': self.published, 
            'author': self.author.username if self.author else 'Unknown',
            'banner': self.banner.url if self.banner else '',  
        }

        MetaTags.objects.update_or_create(url=url, defaults=defaults)

    def delete(self, *args, **kwargs):
        if self.banner and os.path.isfile(self.banner.path) and self.banner != 'defaults/blog_default.webp':
            os.remove(self.banner.path)

        
        MetaTags.objects.filter(url=self.url()).delete()
        
        super(Article, self).delete(*args, **kwargs)
            
    


# Create your models here.
class Tag(models.Model):
    '''
    Holds blog tags
    '''
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name='Name', max_length=100, unique=True)
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    slug = models.SlugField(verbose_name='slug', null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    # def url(self):
    #     self.link = reverse('blogs:article',  kwargs={'slug':self.slug})
    #     return self.link

    def save(self, *args, **kwargs):
        value = f'{self.name}'
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
