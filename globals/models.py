from django.db import models
import uuid
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
def validate_image(image):
    file_size = image.file.size
    limit_kb = 512
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)

# Create your models here.
class Global(models.Model):
    """
    Stores site's global information.
    """
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    company_name = models.CharField(verbose_name='Company Name', max_length=100, unique=True)
    show_name = models.BooleanField(verbose_name='show name on navbar', default=False)
    show_logo = models.BooleanField(verbose_name='show logo on navbar', default=True)
    description = models.TextField(verbose_name='description', blank=True)
    address = models.TextField(verbose_name='address')
    email = models.EmailField(verbose_name='email')
    contact_numbers = models.CharField(verbose_name='contact_numbers', blank=True, max_length=100)
    logo = models.ImageField(verbose_name='logo',upload_to='logos', blank=True, validators=[validate_image], null=True)
    google_analytics_tag = models.TextField(verbose_name='google_analytics_tag', blank=True)
    additional_tags = models.TextField(verbose_name='additional_tags', blank=True)
    privacy_policy = RichTextField(verbose_name='privacy policy', blank=True)
    terms_of_service = RichTextField(verbose_name='terms of service', blank=True)
    security = RichTextField(verbose_name='security', blank=True)


