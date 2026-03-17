from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Customer(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    firstname = models.CharField(verbose_name='First name', max_length=100)
    lastname = models.CharField(verbose_name='Last name', max_length=100)
    company_name = models.CharField(verbose_name='Company name', max_length=100)
    
    BRACKET_CHOICES = [
        ('msp', 'MSP'),
        ('it_department', 'IT Department'),
        ('other', 'Other'),
    ]

    bracket = models.CharField(verbose_name='bracket', choices=BRACKET_CHOICES, max_length=25, default='msp')
    
    email = models.EmailField(verbose_name='Email')
    email_verified = models.BooleanField(verbose_name="Email Verified",default=False)
    address = models.TextField(verbose_name='Address', blank=True)
    country = CountryField()
    phone_number = PhoneNumberField(verbose_name='Contact number')
    subdomain = models.CharField(verbose_name='Subdomain', max_length=25)
    number_of_devices = models.IntegerField(verbose_name='Number of devices')
    CONTACT_CHOICES = [
        ('phone', 'Phone'),
        ('email', 'Email'),
    ]
    contact_mode = models.CharField(verbose_name='Contact mode', choices=CONTACT_CHOICES, max_length=25, default='email')
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    slug = models.SlugField(verbose_name='slug', null=True, blank=True)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

    def save(self, *args, **kwargs):
        value = f'{self.unique_id}'
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class ContactUs(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name='Name', max_length=255,null=False,blank=False)
    email = models.EmailField(verbose_name='Email' ,null=False,blank=False)
    phone_number = PhoneNumberField(verbose_name='Contact no.' ,null=False,blank=False)
    company_name = models.CharField(verbose_name="Company Name", max_length=100 ,null=False,blank=False)
    message = models.TextField(verbose_name='Message',null=False,blank=False)
