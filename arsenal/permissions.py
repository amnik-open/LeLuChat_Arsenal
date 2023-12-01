"""Define permissions for arsenal app"""
from rest_framework import permissions
from arsenal.remote_authentication import RemoteUserType
from arsenal.models import Membership


class IsLeluUser(permissions.BasePermission):
    """Define permission for LeluUser"""

    def has_permission(self, request, view):
        return request.user and request.user.type == RemoteUserType.LeluUser.name

class IsReadOnlyMemberOrAdminMember(permissions.BasePermission):
    """Define permission for membership"""

    def has_object_permission(self, request, view, obj):
        try:
            membership = Membership.objects.get(room=obj, member_uuid=request.user.uuid)
            if request.method in permissions.SAFE_METHODS:
                return True
            return membership.is_admin
        except Membership.DoesNotExist:
            return False
