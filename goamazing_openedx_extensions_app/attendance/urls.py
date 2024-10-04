from django.urls import path
from .views import attendance_get, attendance_post
from django.conf import settings

urlpatterns = [
    path('courses/{settings.COURSE_KEY_PATTERN}', attendance_get, name='attendance_get'),  # for GET requests
    path('courses/{settings.COURSE_KEY_PATTERN}', attendance_post, name='attendance_post'),  # for POST requests
]
