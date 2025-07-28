
import time
from django.http import JsonResponse
from collections import defaultdict

class OffensiveLanguageMiddleware:
    """
    Middleware to limit number of POST (message) requests per IP address to 5 per minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = defaultdict(list)  # { ip: [timestamps] }

    def __call__(self, request):
        if request.method == 'POST':
            ip = self.get_ip(request)
            current_time = time.time()

            # Clean up old timestamps (older than 60 seconds)
            self.message_log[ip] = [
                t for t in self.message_log[ip] if current_time - t < 60
            ]

            if len(self.message_log[ip]) >= 5:
                return JsonResponse(
                    {'error': 'Rate limit exceeded: Max 5 messages per minute.'},
                    status=429
                )

            # Log this request
            self.message_log[ip].append(current_time)

        return self.get_response(request)

    def get_ip(self, request):
        """Get the real IP address of the user."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
