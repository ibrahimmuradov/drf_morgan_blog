from rest_framework import permissions

class AccessPermission(permissions.BasePermission):
    message = 'You are not admin.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.email == "admin@gmail.com"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False
