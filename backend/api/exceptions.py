from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework import status, views


class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Item not found'


class ValidationException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Validation Failed'


def exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        exc = ValidationException()

    if isinstance(exc, APIException):
        data = {
            'code': exc.status_code,
        }
        message = getattr(exc, 'message', None)
        if message:
            data['message'] = message

        views.set_rollback()
        return Response(data, status=exc.status_code)
    return None
