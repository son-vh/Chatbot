
from rest_framework import status
from rest_framework.response import Response


class Res:
    def __init__(self):
        self._message_code = 1
        self._message_detail = ''
        self._data = []
        self._status_code = status.HTTP_200_OK

    def set_message_code(self, message_code):
        self._message_code = message_code

    def set_message_detail(self, message_detail):
        self._message_detail = message_detail

    def set_data(self, data):
        self._data = data

    def set_status_code(self, status_code):
        self._status_code = status_code

    def done(self):
        response = {
            'message_code': self._message_code,
            'message_detail': self._message_detail,
            'data': self._data
        }

        return Response(response, status=self._status_code)
