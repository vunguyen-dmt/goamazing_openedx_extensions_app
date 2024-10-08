from datetime import datetime
from django.http import JsonResponse, Http
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from opaque_keys.edx.keys import CourseKey
from common.djangoapps.student.models import CourseEnrollment
from goamazing_openedx_extensions_app.common.insights_db import InsightsDatabase
import json
import logging

log = logging.getLogger('attendance')

# @login_required
# @ensure_csrf_cookie
# def attendance_get(request, *args, **kwargs):
#     return JsonResponse(status=200)
    # course_key_string = kwargs.get('course_key_string')
    # course_key = CourseKey.from_string(course_key_string)
    # enrollment = CourseEnrollment.get_enrollment(request.user, course_key_string)
    # user_is_enrolled = bool(enrollment and enrollment.is_active)

    # error = ''
    # try:
    #     db = InsightsDatabase()
    #     db.connect()
    #     query = 'SELECT * FROM Permission'
    #     results = db.execute_query(query)
    # except Exception as ex:
    #     error = ex.args[1]

    # result = {
    #     "type": "get",
    #     "results": results,
    #     "error": error,
    #     "course_key_string": course_key_string,
    #     "user_is_enrolled": user_is_enrolled,
    #     "userId": request.user.id,
    #     "username": request.user.username
    # }
    # return JsonResponse(result)

@login_required
@ensure_csrf_cookie
def attendance_post(request, *args, **kwargs):
    if request.method == 'POST':
        qr_config_id = kwargs.get('qr_config_id')
        course_key_string = kwargs.get('course_key_string')
        enrollment = CourseEnrollment.get_enrollment(request.user, course_key_string)
        user_is_enrolled = bool(enrollment and enrollment.is_active)

        if not user_is_enrolled:
            return JsonResponse({'error': 'you\'ve not enrolled.'}, status=400)

        request_body = json.loads(request.body.decode('utf8'))
        longitude = request_body["longitude"] if "longitude" in request_body else ""
        latitude = request_body["latitude"] if "latitude" in request_body else ""

        qr_config_id = kwargs.get('qr_config_id')
        if not qr_config_id:
            return JsonResponse({'error': 'Invalid QR'}, status=400)

        utc_now = datetime.now(datetime.timezone.utc)

        db = InsightsDatabase()
        db.connect()

        qr_config = db.execute_query(f"""
            SELECT * FROM AttendanceQRConfig
            WHERE Id = ? AND CourseId = ? AND DueTime <= ?
        """, (qr_config_id, qr_config_id, utc_now), True)

        if not qr_config:
            return JsonResponse({'error': 'The QR does not exist or expired.'}, status=400)

        if qr_config.LocationRequirement == 'yes' and (not longitude or not latitude):
            return JsonResponse({'error': 'Your location is required.'}, status=400)

        try:
            db.execute_query(f"""
                INSERT INTO AttendanceQR (StudentId, AttendanceQRConfigId, CreatedTime, Longitude, Latitude, Status)
                VALUES (?, ?, ?, ?, ?, 'open')
            """, (request.user.id, qr_config_id, utc_now, longitude, latitude), True)
            db.connection.commit()
        except Exception as e:
            log.error("insert attendance qr error: " + str(e))
            return JsonResponse(status=500)

        db.close()
        return JsonResponse(status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
