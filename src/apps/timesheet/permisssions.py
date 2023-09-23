from rest_framework import permissions
from ..user_managment.models.profile import Profile
from guardian.shortcuts import has_permission


# class CustomPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             pass
#         return False

#     def has_object_permission(self, request, view, obj):
#         if request.method not in permissions.SAFE_METHODS:
#             if obj.has_permission(''):
#                 pass
            