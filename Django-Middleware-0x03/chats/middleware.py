import time
from collections import defaultdict
from django.http import JsonResponse

class OffensiveLanguageMiddleware:
    """
    Middleware to limit number of POST requests (messages) from an IP address.
    Max: 5 messages per minute.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_log = defaultdict(list)

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api/messages'):
            ip = self.get_client_ip(request)
            now = time.time()
            window_start = now - 60  # 1 minute window

            # Filter timestamps within last 60 seconds
            self.ip_message_log[ip] = [t for t in self.ip_message_log[ip] if t > window_start]

            if len(self.ip_message_log[ip]) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Max 5 messages per minute."},
                    status=429
                )

            self.ip_message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Get client IP from request headers"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolePermissionMiddleware:
    """
    Middleware to allow only users with 'admin' or 'moderator' roles to access certain actions.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_role = getattr(request.user, 'role', None)
            allowed_roles = ['admin', 'moderator']

            # Apply restriction on admin panel or unsafe HTTP methods
            if request.path.startswith('/admin/') or request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                if user_role not in allowed_roles:
                    return JsonResponse(
                        {'error': 'Access forbidden: insufficient permissions.'},
                        status=403
                    )

        return self.get_response(request)
