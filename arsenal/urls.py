"""Specify urls for users app"""
from django.urls import path
from arsenal.views import RoomList, RoomDetail, ChatList, RoomMembership
from arsenal.views import MessagingGate, ChatMessageList


app_name = 'users'

urlpatterns = [
    path('rooms/', RoomList.as_view(), name='room_list'),
    path('rooms/<uuid:uid>/', RoomDetail.as_view(), name='room_detail'),
    path('rooms/<uuid:uid>/chats/', ChatList.as_view(), name='chat_list'),
    path('rooms/<uuid:uid>/members/', RoomMembership.as_view(), name='room_membership'),
    path('chats/<uuid:uid>/messages/', ChatMessageList.as_view(), name='chat_message_list'),
    path('gates/messages/', MessagingGate.as_view(), name='messaging_gate')
]
