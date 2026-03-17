from django.urls import path
from .views import EmailValidationView

app_name='customers'

urlpatterns = [
    path('email-validator/',EmailValidationView.as_view(),name='email_validator'),
]
