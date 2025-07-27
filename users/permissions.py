from rest_framework import permissions


class IsModerDRF(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsOwnerDRF(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user