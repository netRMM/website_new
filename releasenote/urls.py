from django.urls import path
from. import views

app_name='releasenote'

urlpatterns = [
    # Release Notes
    path('releasenotes/', views.releasenotes, name='releasenotes'),
    path('releasenotes/<release_id>', views.releasenote_detailed, name='releasenote_detailed'),
]
