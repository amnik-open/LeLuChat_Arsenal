"""Define serializers for arsenal app"""
from rest_framework import serializers
from arsenal.models import Room, Membership


class MembershipSerializer(serializers.ModelSerializer):
    """Serializer for Membership model"""

    email = serializers.EmailField(source='member_email')
    class Meta:
        model = Membership
        fields = ["email", "is_admin"]


class RoomSerializerList(serializers.ModelSerializer):
    """Serializer for Room model"""

    uuid = serializers.UUIDField(source='room_uuid', read_only=True)

    class Meta:
        model = Room
        fields = ["uuid", "url", "name"]

    def create(self, validated_data):
        return Room.objects.create(name=validated_data['name'], url=validated_data['url'],
                                   member_uuid=validated_data['member_uuid'],
                                   member_email=validated_data['member_email'],
                                   is_admin=validated_data['is_admin'])

class RoomSerializerDetail(serializers.ModelSerializer):
    """Detail serializer for Room model"""

    members = MembershipSerializer(many=True, source="membership")
    uuid = serializers.UUIDField(source='room_uuid', read_only=True)

    class Meta:
        model = Room
        fields = ["uuid", "url", "name", 'members']
