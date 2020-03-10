from datetime import datetime

import requests
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from chatbot.business import Business
from chatbot.helper.constants import API_URL
from chatbot.helper.helper import Helper
from chatbot.helper.response import Res
from configs.log_config import logger

log = logger()


@api_view(['GET'])
def chatbot(request):
    query = request.GET.get('query', '')
    nowaday = datetime.now()

    print(query)
    user_id = request.user.id
    print(user_id)

    PARAMS = {'query': query}
    res = requests.get(
        url=API_URL.format(user_id),
        params=PARAMS,
        verify=False
    ).json()

    print(res)

    # Trả vê câu nói bình thường
    if res[0]['text'] != 'action':
        answer = str(res[0]['text'])
        Helper.write_history_log(query, answer, nowaday)
        return JsonResponse(res, safe=False)

    else:
        try:
            suggest_information = res[0]['buttons'][0]['suggest_information']
            name = res[0]['buttons'][0]['name']

            date = suggest_information.get('date')
            start_time = suggest_information.get('time')
            duration = suggest_information.get('duration')
            room_id = suggest_information.get('room_id')
            size = suggest_information.get('size')
            booking_id = suggest_information.get('booking_id')
            kwargs = {
                'size__gte': size,
            }
            new_kwargs = {
                'room__size__gte': size,
            }

            if name == 'find_available_room':

                # res[0]['buttons'][0]['rooms'] = Business.find_available_room(date, start_time, duration, **kwargs)
                res[0]['buttons'][0]['rooms'] = Business.find_available_room(date, **kwargs)
                res[0]['text'] = 'Tôi tìm được các phòng này còn trống theo yêu cầu của bạn'

                return JsonResponse(res, safe=False)
            elif name == 'booking_room':

                if room_id is None:

                    booking_room_by_size = Business.book_room_by_size(date, start_time, duration, user_id, **kwargs)

                    if len(booking_room_by_size) != 0:
                        res[0]['buttons'][0]['rooms'] = booking_room_by_size
                        res[0]['result'] = 'book_success'
                        res[0]['text'] = 'Tôi đã đặt phòng giúp bạn rồi ạ. Đây là thông tin về phòng họp của bạn nhé'
                    else:
                        res[0]['buttons'][0]['rooms'] = []
                        res[0]['result'] = 'book_fail'
                        res[0]['text'] = 'Bạn đặt phòng thất bại'

                    return JsonResponse(res, safe=False)

                else:

                    booking_room_by_id = Business.book_room_by_id(date, start_time, duration, room_id, user_id,
                                                                  **new_kwargs)

                    if len(booking_room_by_id) != 0:

                        res[0]['buttons'][0]['rooms'] = booking_room_by_id

                        res[0]['result'] = 'book_success'
                        res[0]['text'] = 'Tôi đã đặt phòng giúp bạn rồi ạ. Đây là thông tin về phòng họp của bạn nhé'
                    else:
                        res[0]['buttons'][0]['rooms'] = []

                        res[0]['result'] = 'book_fail'
                        res[0]['text'] = 'Bạn đã đặt phòng thất bại'

                    return JsonResponse(res, safe=False)

            elif name == 'find_booked_room':
                booked_room = Business.find_booked_room(date, user_id)
                if len(booked_room) != 0:
                    res[0]['buttons'][0]['rooms'] = booked_room
                    if res[0]['buttons'][0].get('mes') is None:
                        res[0]['text'] = 'Đây là thông tin phòng bạn đã đặt'
                    else:
                        res[0]['text'] = res[0]['buttons'][0].get('mes')
                else:
                    res[0]['buttons'][0]['rooms'] = booked_room
                    if res[0]['buttons'][0].get('mes') is None:
                        res[0]['text'] = 'Ngày hôm nay bạn chưa đặt phòng'
                    else:
                        res[0]['text'] = res[0]['buttons'][0].get('mes')

                return JsonResponse(res, safe=False)

            elif name == 'cancel_room_by_booking_id':
                deleted_room = Business.remove_room(booking_id, user_id)
                if len(deleted_room) != 0:
                    res[0]['buttons'][0]['rooms'] = deleted_room
                    res[0]['text'] = 'Tôi đã hủy phòng họp giúp bạn thành công. Bạn có cần tôi giúp thêm gì nữa không ?'
                else:
                    res[0]['text'] = 'Phòng này bạn chưa đặt.Hủy phòng thất bại'

                return JsonResponse(res, safe=False)

        except Exception as ex:
            log.error(ex)


@api_view(['GET'])
def find_all_room(request):
    res = Res()
    data = Business.find_list_room()
    res.set_data(data)
    return res.done()


@api_view(['POST'])
def find_duration_time(request):
    room_id = request.POST.get('room_id')
    res = Res()
    data = Business.find_booked_duration_time(room_id)
    res.set_data(data)
    return res.done()


@api_view(['POST'])
def edit_room(request):
    date = request.POST.get('date')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    booking_room_id = request.POST.get('id')

    res = Res()
    data = Business.edit_end_time(booking_room_id, date, start_time, end_time)
    if data == 0:
        res.set_message_code(0)
        res.set_message_detail('fail')
        # res.set_status_code(status.HTTP_404_NOT_FOUND)
    else:
        res.set_message_detail('success')
        # res.set_status_code(status.HTTP_404_NOT_FOUND)

    return res.done()


@api_view(['POST'])
def update_status(request):
    booking_room_id = request.POST.get('id')
    st = request.POST.get('status')
    res = Res()
    data = Business.updated_status(booking_room_id, st)
    res.set_message_detail('success')
    return res.done()


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def check_exist_room(request):
    room_id = request.POST.get('room_id')
    res = Res()

    if not Business.check_room(room_id):
        res.set_message_code(0)
        res.set_message_detail('fail')
        res.set_data(Business.find_list_room())
    else:
        res.set_message_detail('success')

    return res.done()


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def get_room_size(request):
    room_id = request.POST.get('room_id')
    # size = request.POST.get('size')
    res = Res()

    data = Business.get_room_size_by_room_id(room_id)
    print(len(data))
    if len(data) == 0:
        res.set_data(data)
        res.set_message_code(0)
        res.set_status_code(status.HTTP_404_NOT_FOUND)
    else:
        res.set_data(data[0])

    return res.done()


# https://stackoverflow.com/questions/27085219/how-can-i-disable-authentication-in-django-rest-framework
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_max_room_size(request):
    res = Res()
    data = Business.get_max_size()
    res.set_data(data)
    return res.done()


def v2(request):
    data = {
        'message': '1',
        'error': '2'
    }
    return JsonResponse(data, safe=False)
