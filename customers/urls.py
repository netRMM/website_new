from django.urls import path
from .views import *

app_name = "customers"

urlpatterns = [
    # path('', views.customers, name='customers'),
    path('contact-us/', contact_us, name='contact_us'),
    path('get-started/', add_customer, name='add_customer'),
    path('activate/<uidb64>/<token>',activate,name="activate"),
    # path('<slug>/edit', views.edit_customer, name='edit_customer'),
]
