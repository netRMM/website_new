from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
import uuid
# Create your models here.

MONTHS = [
    ('january','January'),
    ('february','February'),
    ('march','March'),
    ('april','April'),
    ('may','May'),
    ('june','June'),
    ('july','July'),
    ('august','August'),
    ('september','September'),
    ('october','October'),
    ('november','November'),
    ('december','December'),
]


class YearField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if value is not None and (value < 1000 or value > 9999):
            raise ValueError('Year must be a four-digit number.')
            
    def formfield(self, **kwargs):
        defaults = {'min_value': 1000, 'max_value': 9999}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class ReleaseYear(models.Model):
    year = YearField(unique=True)

    def __str__(self):
        return str(self.year)


class ReleaseNote(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    title = models.CharField(verbose_name='Release Note Title', max_length=100)
    body = RichTextField()
    month = models.CharField(verbose_name='Release Month',choices=MONTHS , max_length=50)
    version = models.CharField(verbose_name='Release Version',max_length=50,unique=True)
    year = models.ForeignKey(ReleaseYear,verbose_name='Release Year' , on_delete=models.CASCADE)
