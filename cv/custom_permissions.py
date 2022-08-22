from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):

    """
    Custom permission to only allow authenticated owners of an object or Admin.
    """
    def has_object_permission(self, request, view, obj):

        try:
            if not request.user.is_authenticated:
                return False
            if hasattr(obj, "user"):
                return obj.user == request.user
            elif hasattr(obj, "user_id"):
                return obj.user_id == request.user
            elif hasattr(obj, "created_by"):
                return obj.created_by == request.user
            return request.user.is_superuser
        except Exception:
            return False