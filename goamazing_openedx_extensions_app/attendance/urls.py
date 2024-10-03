from django.urls import path
from .views import attendance_get, attendance_post

urlpatterns = [
    path('', attendance_get, name='attendance_get'),  # for GET requests
    path('', attendance_post, name='attendance_post'),  # for POST requests
]
