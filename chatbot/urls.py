from django.urls import path

from chatbot import views

urlpatterns = [
    path('v1', views.chatbot, name="chatbot"),
    path('find_all_room', views.find_all_room, name="find_all_room"),
    path('find_duration_time', views.find_duration_time, name="find_duration_time"),
    path('edit_room', views.edit_room, name="edit_room"),
    path('update_status', views.update_status, name="update_status"),
    path('check_exist_room', views.check_exist_room, name="check_exist_room"),
    path('get_room_size', views.get_room_size, name="get_room_size"),
    path('get_max_room_size', views.get_max_room_size, name="get_max_room_size"),
    path('v2', views.v2, name="v2"),
]
