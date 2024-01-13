from rest_framework.permissions import BasePermission



class IsOwnerOrReadOnly(BasePermission):
    # Custom permission to only allow the owner of an object editing it
    def has_permission(self, request, view):
        return True  # Allowing anyone to perform read-only

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin