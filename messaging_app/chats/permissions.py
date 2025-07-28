# chats/permissions.py
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom object-level permission: Only owners can update or delete.
    Others can read only (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True

        # Explicitly restrict unsafe methods
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return (
                request.user and
                request.user.is_authenticated and
                obj.owner == request.user  # Adjust 'owner' as per your model
            )

        # Default deny
        return False
