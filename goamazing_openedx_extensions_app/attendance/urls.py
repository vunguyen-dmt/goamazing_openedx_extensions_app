from django.urls import path, re_path
from .views import attendance_get, attendance_post
from django.conf import settings

urlpatterns = [
    re_path(fr'courses/{settings.COURSE_KEY_PATTERN}$', attendance_get, name='attendance_get'),  # for GET requests
    re_path(fr'courses/{settings.COURSE_KEY_PATTERN}$', attendance_post, name='attendance_post'),  # for POST requests
]
