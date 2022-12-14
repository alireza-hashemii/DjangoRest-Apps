from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
class SuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return super().has_permission(request, view)
        else:
            return request.method in SAFE_METHODS




class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
            if request.user and  obj.review_author == request.user:
                return super().has_object_permission(request, view,obj)
            else:
                return request.method in SAFE_METHODS
                
    