"""Define model for arsenal app"""
import uuid
from django.db import models
from rpc_client.membership import RpcClientMembership


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

    def update_members(self, room, members, add):
        email_members = ""
        is_admin_members = []
        for member in members:
            try:
                ms = Membership.objects.get(room=room, member_email=member['member_email'])
                if add:
                    ms.is_admin = member['is_admin']
                    ms.save()
                else:
                    ms.delete()
            except Membership.DoesNotExist:
                if add:
                    email_members += " " + member['member_email']
                    is_admin_members.append(member["is_admin"])
        email_members = email_members.strip()
        if len(email_members) != 0:
            rpc_members = RpcClientMembership().call(email_members)
            rpc_members = rpc_members.split(" ")
            email_members = email_members.split(" ")
            for i, v in enumerate(rpc_members):
                Membership.objects.create(room=room, member_email=email_members[i],
                                          member_uuid=uuid.UUID(v).hex,is_admin=is_admin_members[i])
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

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="memberships")
    member_uuid = models.UUIDField(blank=False, null=False)
    member_email = models.EmailField(blank=False, null=False)
    is_admin = models.BooleanField(default=False)
    member_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['room', 'member_uuid'], name='unique uuid membership'),
            models.UniqueConstraint(fields=['room', 'member_email'], name='unique email '
                                                                          'membership'),
        ]


class ChatManager(models.Manager):
    """Manager for Chat model"""

    def create(self, room, owner, name):
        chat = Chat(room=room, owner=owner, name=name)
        chat.save()
        return chat


class Chat(models.Model):
    """Define Chat model"""

    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='chats')
    owner = models.UUIDField(unique=True)
    name = models.CharField(max_length=200)
    chat_uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    start_time = models.DateTimeField(auto_now_add=True)
