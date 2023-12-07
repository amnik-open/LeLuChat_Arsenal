"""Define serializers for arsenal app"""
from rest_framework import serializers
from arsenal.models import Room, Membership, Chat, Message


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

    members = MembershipSerializer(many=True, source="memberships")
    uuid = serializers.UUIDField(source='room_uuid', read_only=True)

    class Meta:
        model = Room
        fields = ["uuid", "url", "name", 'members']


class RoomMembershipSerializer(serializers.ModelSerializer):
    """Define serializer for membership of Room model"""

    members = MembershipSerializer(many=True, source="memberships")

    class Meta:
        model = Room
        fields = ["members"]

    def update(self, instance, validated_data):
        return Room.objects.update_members(room=instance,
                                           members=validated_data['memberships'],
                                           add=validated_data['add'])


class ChatListSerializer(serializers.ModelSerializer):
    """Define serializer for chat model"""

    owner = serializers.UUIDField()
    chat_uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = Chat
        fields = ['chat_uuid', 'name', 'owner', 'start_time']

    def create(self, validated_data):
        return Chat.objects.create(room=validated_data['room'], owner=validated_data['owner'],
                                   name=validated_data['name'])


class ChatDetailSerializer(serializers.ModelSerializer):
    """Define serializer for Chat detail"""

    owner = serializers.UUIDField()
    chat_uuid = serializers.UUIDField(read_only=True)
    auth_token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Chat
        fields = ['owner', 'chat_uuid', 'name', 'auth_token', 'start_time']

    def get_auth_token(self, obj):
        return self.context.get('auth_token')


class MessageGateSerializer(serializers.Serializer):
    """Define serializer for messaging gate"""

    room = serializers.UUIDField()
    chat = serializers.UUIDField()


class ChatMessageSerializer(serializers.ModelSerializer):
    """Define serializer for chat in message"""

    chat_uuid = serializers.UUIDField()
    class Meta:
        model = Chat
        fields = ['chat_uuid']


class MessageSerializer(serializers.ModelSerializer):
    """Define serializer for message"""

    chat = ChatMessageSerializer()
    class Meta:
        model = Message
        fields = ['sender', 'text', 'chat', 'timestamp']

    def create(self, validated_data):
        return Message.objects.creat_by_chat_uuid(sender=validated_data['sender'],
                                                  chat_uuid=validated_data['chat']['chat_uuid'],
                                                  text=validated_data['text'])

class MessageListSerializer(serializers.ModelSerializer):
    """Define serializer for message list"""

    class Meta:
        model = Message
        fields = ['sender', 'text',  'timestamp']


class ChatMessageListSerializer(serializers.ModelSerializer):
    """Define serializer to list messages of chat"""

    messages = MessageListSerializer(many=True)

    class Meta:
        model = Chat
        exclude = ['id', 'room']
