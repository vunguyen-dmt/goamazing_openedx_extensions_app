from django.urls import path, include
from goamazing_openedx_extensions_app.attendance.views import AttendanceView

urlpatterns = [
    path(r'', AttendanceView.as_view(), name='attendance'),
]
