from rest_framework import serializers

from .models import Room, BookingRoom


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class BookingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRoom
        fields = '__all__'


class BookingRoomTimeSerializer(BookingRoomSerializer):
    class Meta:
        model = BookingRoom
        fields = ('id', 'start_time', 'end_time', 'date', 'title', 'content', 'reason', 'status', 'owner')
