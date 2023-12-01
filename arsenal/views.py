"""Define API views for arsenal app"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from arsenal.serializers import RoomSerializerList, RoomSerializerDetail
from arsenal.models import Room
from arsenal.permissions import IsLeluUser, IsReadOnlyMemberOrAdminMember


class RoomList(APIView):
    """API for Room model"""

    permission_classes = [permissions.IsAuthenticated, IsLeluUser]

    def get(self, request, format=None):
        rooms = Room.objects.filter(membership__member_email=request.user.email)
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
