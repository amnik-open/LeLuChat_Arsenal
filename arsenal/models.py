"""Define model for arsenal app"""
import uuid
from django.db import models


class RoomManager(models.Manager):
    """Manger for Room model"""

    def create(self, **kwargs):
        room = Room(name=kwargs['name'], url=kwargs['url'])
        room.save()
        membership = Membership(room=kwargs['room'], member_uuid=kwargs['member_uuid'],
                                member_email=kwargs['member_email'],
                                is_admin=kwargs['is_admin'])
        membership.save()
        return room

    def update(self, room, name, url, memberships):
        room.name = name
        room.url = url
        room_memberships = room.membership.all()
        uuid_isadmin = {}
        for membership in memberships:
            uuid_isadmin[membership['member_uuid']] = membership['is_admin']
        for rm in room_memberships:
            if rm.member_uuid not in uuid_isadmin:
                room.membership.remove(rm.member_uuid)
            else:
                membership = Membership.objects.get(room=room, member_uuid=rm.member_uuid)
                if membership.is_admin != uuid_isadmin[rm.is_admin]:
                    membership.is_admin = uuid_isadmin[rm.is_admin]
                    membership.save()
                del uuid_isadmin[rm.member_uuid]
        for uuid, is_admin in uuid_isadmin.values():
            membership = Membership(room=room, member_uuid=uuid, is_admin=is_admin)
            membership.save()
        return room

    def update_members(self, room, memberships, add):
        for membership in memberships:
            if add:
                ms, _ = Membership.objects.get_or_create(room=room, member_uuid=membership[
                    'uuid'],member_email=membership['email'])
                ms.is_admin = membership['is_admin']
                ms.save()
            else:
                ms = Membership.objects.get(room=room, member_uuid=membership['uuid'],
                                                     member_email=membership['email'])
                if ms:
                    ms.delete()
        return room


class Room(models.Model):
    """Define Room model"""

    name = models.CharField(max_length=50)
    url = models.URLField(max_length=200, unique=True)
    room_uuid = models.UUIDField(unique=True, default=uuid.uuid4)

    objects = RoomManager()

    def __str__(self):
        return self.name


class Membership(models.Model):
    """Define membership of LuluUser in Room"""

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="membership")
    member_uuid = models.UUIDField(blank=False, null=False)
    member_email = models.EmailField(blank=False, null=False)
    is_admin = models.BooleanField(default=False)
    member_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['room', 'member_uuid'], name='unique membership')
        ]
