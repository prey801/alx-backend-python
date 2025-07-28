# chats/middleware.py

from datetime import datetime, time
from django.http import HttpResponse


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define allowed time range (e.g., 08:00 to 18:00)
        self.start_time = time(8, 0, 0)
        self.end_time = time(18, 0, 0)

    def __call__(self, request):
        now = datetime.now().time()
        if not self.start_time <= now <= self.end_time:
            return HttpResponse("Access is restricted outside of working hours (8 AM - 6 PM).", status=403)
        return self.get_response(request)
