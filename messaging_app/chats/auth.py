
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT auth to reject inactive or banned users.
    """
    def authenticate(self, request):
        result = super().authenticate(request)

        if result is None:
            return None  # No token provided, fallback to anonymous

        user, token = result

        if not user.is_active:
            raise AuthenticationFailed('User account is disabled.')

        # Optional: Check user roles, email verification, etc.
        # if not user.is_verified:
        #     raise AuthenticationFailed('Email is not verified.')

        return (user, token)
