from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.exceptions import ValidationError

def validate_image(image):
    file_size = image.file.size
    limit_kb = 512
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)

# Create your models here.
class Profile(models.Model):
    '''
    Holds user profile data.
    '''
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, verbose_name='user', on_delete=models.CASCADE, null=True)
    designation = models.CharField(verbose_name='designation', max_length=50, blank=True)
    bio = models.TextField(verbose_name='bio', blank=True)
    picture = models.ImageField(verbose_name='picture',upload_to='users/profiles', default='defaults/user_default.webp', validators=[validate_image])