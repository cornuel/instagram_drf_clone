from rest_framework import permissions

class IsAccountOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'profile'):
            # obj is a Post or a Comment
            return obj.profile.user == request.user or request.user.is_staff
        elif hasattr(obj, 'user'):
            # obj is a Profile
            return obj.user == request.user or request.user.is_staff
        else:
            return obj.username == request.user or request.user.is_staff