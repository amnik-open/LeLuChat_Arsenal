"""Define API views for arsenal app"""
import json
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from django.conf import settings
from arsenal.serializers import RoomSerializerList, RoomSerializerDetail, ChatListSerializer
from arsenal.serializers import ChatDetailSerializer, RoomMembershipSerializer
from arsenal.serializers import MessageGateSerializer, ChatMessageListSerializer
from arsenal.models import Room, Chat
from arsenal.permissions import IsLeluUser, IsReadOnlyMemberOrAdminMember, IsChatOwnerOrRoomMember
from arsenal.permissions import IsGetAuthenticatedLeluUserOrPost, IsMemberChatRoomOrChatowner
from rpc_client.websiteuser_register import RpcClientWebUserReg


log = logging.getLogger(__name__)


class RoomList(APIView):
    """API for Room model"""

    permission_classes = [permissions.IsAuthenticated, IsLeluUser]

    def get(self, request, format=None):
        rooms = Room.objects.filter(memberships__member_email=request.user.email)
        serializer = RoomSerializerList(rooms, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RoomSerializerList(data=request.data)
        if serializer.is_valid():
            serializer.save(member_uuid=request.user.uuid, member_email=request.user.email,
                            is_admin=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetail(APIView):
    """API for Room with detail"""

    permission_classes = [permissions.IsAuthenticated, IsLeluUser, IsReadOnlyMemberOrAdminMember]

    def get(self, request, uid, format=None):
        room = get_object_or_404(Room, room_uuid=uid)
        self.check_object_permissions(self.request, room)
        serializer = RoomSerializerDetail(room)
        return Response(serializer.data)

    def delete(self, request, uid, format=None):
        room = get_object_or_404(Room, room_uuid=uid)
        self.check_object_permissions(self.request, room)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RoomMembership(APIView):
    """Define API of membership of Room model"""

    permission_classes = [permissions.IsAuthenticated, IsReadOnlyMemberOrAdminMember]

    def patch(self, request, uid, format=None):
        room = get_object_or_404(Room, room_uuid=uid)
        self.check_object_permissions(self.request, room)
        serializer = RoomMembershipSerializer(room, data=request.data)
        if serializer.is_valid():
            r = serializer.save(add=True)
            return Response(RoomSerializerDetail(r).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uid, format=None):
        room = get_object_or_404(Room, room_uuid=uid)
        self.check_object_permissions(self.request, room)
        serializer = RoomMembershipSerializer(room, data=request.data)
        if serializer.is_valid():
            r = serializer.save(add=False)
            return Response(RoomSerializerDetail(r).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatList(APIView):
    """Define API for chat model"""

    permission_classes = [IsGetAuthenticatedLeluUserOrPost, IsReadOnlyMemberOrAdminMember]

    def get(self, request, uid, format=None):
        room = get_object_or_404(Room, room_uuid=uid)
        self.check_object_permissions(self.request, room)
        serializer = ChatListSerializer(room.chats, many=True)
        return Response(serializer.data)

    def post(self, request, uid):
        room = get_object_or_404(Room, room_uuid=uid)
        chat_num = room.chats.count()
        name = settings.DEFAULT_PREFIX_CHAT_NAME + str(chat_num + 1)
        try:
            rpc = RpcClientWebUserReg()
            user = json.loads(rpc.call(name))
        except Exception as e:
            log.exception(e)
            return Response("{msg: RPC connection to leluchat_auth has problem}",
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        data = {'owner': user['uuid'], 'name': name}
        serializer = ChatListSerializer(data=data)
        if serializer.is_valid():
            chat = serializer.save(room=room)
            s = ChatDetailSerializer(chat, context={'auth_token': user['auth_token']})
            return Response(s.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatMessageList(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMemberChatRoomOrChatowner]
    def get(self, request, uid, format=None):
        chat = get_object_or_404(Chat, chat_uuid=uid)
        self.check_object_permissions(self.request, chat)
        serializer = ChatMessageListSerializer(chat)
        return Response(serializer.data)


class MessagingGate(APIView):
    """Class for Messaging Gate API"""

    permission_classes = [permissions.IsAuthenticated, IsChatOwnerOrRoomMember]

    def post(self, request, format=None):
        serializer = MessageGateSerializer(data=request.data)
        if serializer.is_valid():
            get_object_or_404(Room, room_uuid=request.data['room'])
            chat = get_object_or_404(Chat, chat_uuid=request.data['chat'])
            self.check_object_permissions(self.request, chat)
            sender = json.dumps(request.user.to_message_sender_dict())
            return Response(sender)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
