from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsModeratorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['moderator', 'admin']