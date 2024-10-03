from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

@login_required
@ensure_csrf_cookie
def attendance_get(request):
    result = {
        "type": "get",
        "userId": request.user.id,
        "username": request.user.username
    }
    return JsonResponse(result)

@login_required
def attendance_post(request):
    # Check if the request method is POST
    if request.method == 'POST':
        result = {
            "type": "post",
            "userId": request.user.id,
            "username": request.user.username
        }
        return JsonResponse(result)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
