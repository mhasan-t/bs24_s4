from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 1

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user_id == request.user.id
