from django.urls import path
from .views import *

app_name = 'docs'

urlpatterns = [
    path('',all_docs,name='all_docs'),
    path('<cat>/<doc>',document_view,name='document_view'),
    
]
