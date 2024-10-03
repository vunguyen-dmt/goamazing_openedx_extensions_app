"""
URLs for goamazing_openedx_extensions_app.
"""
from django.urls import re_path  # pylint: disable=unused-import
from django.views.generic import TemplateView  # pylint: disable=unused-import
from django.urls import path, include

urlpatterns = [
    # TODO: Fill in URL patterns and views here.
    # re_path(r'', TemplateView.as_view(template_name="goamazing_openedx_extensions_app/base.html")),
    path('attendance/', include('goamazing_openedx_extensions_app.attendance.urls')),  # Include the app's API URLs
]
