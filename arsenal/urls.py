"""Specify urls for users app"""
from django.urls import path
from arsenal.views import RoomList, RoomDetail


app_name = 'users'

urlpatterns = [
    path('rooms/', RoomList.as_view(), name='room_list'),
    path('rooms/<uuid:uid>/', RoomDetail.as_view(), name='room_detail'),
]
