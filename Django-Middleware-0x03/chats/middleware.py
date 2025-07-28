# chats/middleware.py

from datetime import datetime
from django.http import JsonResponse

class RestrictAccessByTimeMiddleware:
    """
    Restrict API access to working hours: Monday–Friday, 9:00 AM–5:00 PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now()
        weekday = now.weekday()  # Monday=0, Sunday=6
        hour = now.hour

        if weekday >= 5 or hour < 9 or hour >= 17:
            return JsonResponse({'error': 'Access not allowed at this time.'}, status=403)

        response = self.get_response(request)
        return response
