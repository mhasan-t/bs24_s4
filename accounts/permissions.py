from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs.get('pk', None)
        return pk == request.user.id
