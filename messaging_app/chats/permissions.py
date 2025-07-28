
from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to users with is_staff=True.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsInGroup(permissions.BasePermission):
    """
    Generic permission to check if user is in a specific group.
    Usage: Add custom logic or subclass this.
    """
    group_name = None  # Override this in subclasses

    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name=self.group_name).exists()


class IsModerator(IsInGroup):
    """
    Example: Allow only moderators.
    """
    group_name = 'Moderators'


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only object owner can write; others can read-only.
    """
    def has_object_permission(self, request, view, obj):
        # Safe methods like GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user  # Adjust 'owner' if your model uses a different field
