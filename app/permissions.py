from rest_framework import permissions

class IsAccountOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.profile.user == request.user or request.user.is_staff