from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admins to perform certain actions
    """
    def has_permission(self, request, view):
        # Allow all read operations
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only admins can modify roles
        return request.user.is_authenticated and request.user.role == 'admin'