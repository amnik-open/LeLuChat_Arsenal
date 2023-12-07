"""Define permissions for arsenal app"""
from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed
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

class IsGetAuthenticatedLeluUserOrPost(permissions.BasePermission):
    """Define permission for post request chat"""

    def has_permission(self, request, view):
        if request.method == 'GET':
            return (request.user and request.user.is_authenticated and request.user.type ==
                    RemoteUserType.LeluUser.name)
        if request.method == 'POST':
            return True
        else:
            raise MethodNotAllowed(request.method)

class IsMemberChatRoomOrChatowner(permissions.BasePermission):
    """Define permission for detail of chat"""

    def has_object_permission(self, request, view, obj):
        if request.user.type == RemoteUserType.LeluUser.name:
            try:
                Membership.objects.get(room=obj.room, member_uuid=request.user.uuid)
                return True
            except Membership.DoesNotExist:
                return False
        if request.user.type == RemoteUserType.WebsiteUser.name:
            return obj.owner == request.user.uuid
        else:
            return False


class IsChatOwnerOrRoomMember(permissions.BasePermission):
    """Define permission for messaging gate"""
    def has_object_permission(self, request, view, obj):
        if str(obj.room.room_uuid) != request.data['room']:
            return False
        if request.user.type == RemoteUserType.WebsiteUser.name:
            return str(obj.owner) == request.user.uuid
        if request.user.type == RemoteUserType.LeluUser.name:
            try:
                Membership.objects.get(room=obj.room, member_uuid=request.user.uuid)
                return True
            except Membership.DoesNotExist:
                return False
        return False
