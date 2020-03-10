from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    room_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=25)
    size = models.IntegerField()
    image = models.CharField(max_length=200)
    device = models.CharField(max_length=200)
    type = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'room'


class BookingRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    delete = models.BooleanField(default=True)
    status = models.IntegerField()
    title = models.CharField(max_length=500)
    content = models.CharField(max_length=500)
    reason = models.CharField(max_length=500)
    owner = models.CharField(max_length=200, default='')

    class Meta:
        unique_together = ('room', 'date', 'start_time')
        db_table = 'booking_room'
