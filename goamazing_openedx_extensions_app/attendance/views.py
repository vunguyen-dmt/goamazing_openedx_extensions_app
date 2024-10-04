from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from opaque_keys.edx.keys import CourseKey
from common.djangoapps.student.models import CourseEnrollment
from common.insights_db import InsightsDatabase

@login_required
@ensure_csrf_cookie
def attendance_get(request, *args, **kwargs):
    course_key_string = kwargs.get('course_key_string')
    course_key = CourseKey.from_string(course_key_string)
    enrollment = CourseEnrollment.get_enrollment(request.user, course_key_string)
    user_is_enrolled = bool(enrollment and enrollment.is_active)

    error = ''
    try:
        db = InsightsDatabase()
        db.connect()
        query = 'SELECT * FROM Permission'
        results = db.execute_query(query)
    except Exception as ex:
        error = ex.args[1]

    result = {
        "type": "get",
        "results": results,
        "error": error,
        "course_key_string": course_key_string,
        "user_is_enrolled": user_is_enrolled,
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
