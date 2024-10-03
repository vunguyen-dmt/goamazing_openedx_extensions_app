from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

class AttendanceView(APIView):
    @login_required
    @ensure_csrf_cookie
    def get(self, request):
        result = {
            "type": "get",
            "userId" : request.user.id,
            "username": request.user.username
        }

        return JsonResponse(result)

    @login_required
    def post(self, request):
        result = {
            "type": "post",
            "userId" : request.user.id,
            "username": request.user.username
        }

        return JsonResponse(result)
