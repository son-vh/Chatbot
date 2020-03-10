from datetime import datetime

from django.db.models import Q, Max

from chatbot.helper.helper import Helper
from chatbot.models import BookingRoom, Room
from chatbot.serializers import RoomSerializer, BookingRoomSerializer, \
    BookingRoomTimeSerializer
from configs.log_config import logger

log = logger()


class Business:

    # @staticmethod
    # def find_available_room(date, start_time, duration=None, **kwargs):
    #     new_kwargs = {}
    #     try:
    #         for k, v in kwargs.items():
    #             if v is not None:
    #                 new_kwargs[k] = v
    #
    #         end_time = Helper.determine_end_time(start_time, duration)
    #         unavailable_room_ids = BookingRoom.objects.filter(
    #             (Q(start_time__lt=start_time) & Q(end_time__gt=start_time))
    #             | (Q(start_time__lt=end_time) & Q(end_time__gt=end_time))
    #             | (Q(start_time__gte=start_time) & Q(end_time__lte=end_time)),
    #             date=date).values_list('room', flat=True).distinct()
    #
    #         rooms = Room.objects.filter(**new_kwargs).exclude(room_id__in=unavailable_room_ids)
    #
    #     except Exception as ex:
    #         log.error(ex)
    #
    #     return RoomSerializer(rooms, many=True).data

    @staticmethod
    def find_available_room(date, **kwargs):
        new_kwargs = {}
        try:
            for k, v in kwargs.items():
                if v is not None:
                    new_kwargs[k] = v

            unavailable_room_ids = BookingRoom.objects.filter(date=date).values_list('room', flat=True).distinct()
            rooms = Room.objects.filter(**new_kwargs).exclude(room_id__in=unavailable_room_ids)

        except Exception as ex:
            log.error(ex)

        return RoomSerializer(rooms, many=True).data

    @staticmethod
    def book_room_by_id(date, start_time, duration, room_id, user_id, **kwargs):
        result = {}
        new_kwargs = {}

        for k, v in kwargs.items():
            if v is not None:
                new_kwargs[k] = v

        try:
            end_time = Helper.determine_end_time(start_time, duration)
            room_checker = BookingRoom.objects.filter(
                ~(Q(start_time__gte=end_time) | Q(end_time__lte=start_time)),
                date=date,
                **new_kwargs,
                room_id=room_id).exists()

            if not room_checker:
                booking_room = BookingRoom.objects.create(
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    room_id=room_id,
                    status=0,
                    user_id=user_id)

                result = {
                    'room_id': booking_room.room_id,
                    'date': booking_room.date,
                    'start_time': booking_room.start_time,
                    'end_time': booking_room.end_time,
                    'image': booking_room.room.image,
                    'device': booking_room.room.device
                }
            else:
                result = {}

        except Exception as ex:
            log.error(ex)

        print(result)
        return result

    @staticmethod
    def book_room_by_size(date, start_time, duration, user_id, **kwargs):
        result = {}
        try:
            room = Business.find_available_room(date, start_time, duration, **kwargs)
            if len(room) != 0:
                end_time = Helper.determine_end_time(start_time, duration)
                room_id = room[0]['room_id']
                print(room_id)
                booking_room = BookingRoom.objects.create(date=date,
                                                          start_time=start_time,
                                                          end_time=end_time,
                                                          room_id=room_id,
                                                          status=0,
                                                          user_id=user_id)
                result = {
                    'room_id': booking_room.room_id,
                    'date': booking_room.date,
                    'start_time': booking_room.start_time,
                    'end_time': booking_room.end_time,
                    'image': booking_room.room.image,
                    'device': booking_room.room.device
                }
            else:
                result = {}

        except Exception as ex:
            log.error(ex)

        return result

    @staticmethod
    def find_booked_room(date, user_id):
        if date is None:
            booking_room = BookingRoom.objects.filter(user_id=user_id)
        else:
            booking_room = BookingRoom.objects.filter(date=date, user_id=user_id)

        serializer = BookingRoomSerializer(booking_room, many=True)
        return serializer.data

    # @staticmethod
    # def remove_room(date, start_time):
    #     room = BookingRoom.objects.filter(
    #         (Q(start_time__lte=start_time) & Q(end_time__gte=start_time)),
    #         date=date)
    #     for index in room:
    #         index.delete = False
    #         index.save()
    #     serializer = BookingRoomSerializer(room, many=True)
    #     return serializer.data

    @staticmethod
    def remove_room(booking_id, user_id):
        booking_room = BookingRoom.objects.filter(id=booking_id, user_id=user_id)
        if len(booking_room) != 0:
            booking_room.update(delete=0)
            serializer = BookingRoomSerializer(booking_room, many=True)
            return serializer.data
        else:
            return []

    @staticmethod
    def find_list_room():
        room = Room.objects.all()
        serializer = RoomSerializer(room, many=True)
        return serializer.data

    @staticmethod
    def find_booked_duration_time(room_id):
        booking_room = BookingRoom.objects.filter(room_id=room_id)
        serializer = BookingRoomTimeSerializer(booking_room, many=True)
        return serializer.data

    @staticmethod
    def edit_end_time(booking_room_id, date, start_time, end_time):
        result = 0
        try:
            booking_room = BookingRoom.objects.filter(id=booking_room_id)
            for index in booking_room:
                index.start_time = datetime.strptime(start_time, '%H:%M:%S').time()
                index.end_time = datetime.strptime(end_time, '%H:%M:%S').time()
                index.date = date
                index.save()
            result = 1
        except Exception as ex:
            log.error(ex)
        return result

    @staticmethod
    def check_room(room_id):
        room_checker = Room.objects.filter(room_id=room_id).exists()
        if not room_checker:
            return False
        else:
            return True

    @staticmethod
    def get_room_size_by_room_id(room_id):
        room_checker = Room.objects.filter(room_id=room_id).exists()
        if not room_checker:
            return []
        else:
            room_size = list(Room.objects.filter(room_id=room_id))[0].size
            return [room_size]

    @staticmethod
    def get_max_size():
        room_size = Room.objects.all().aggregate(Max('size'))
        print(room_size['size__max'])
        return room_size['size__max']

    @staticmethod
    def updated_status(booking_room_id, status):
        BookingRoom.objects.filter(id=booking_room_id).update(status=status)
