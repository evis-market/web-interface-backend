from rest_framework.response import Response
from rest_framework.views import exception_handler
from pprint import pprint


def default_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:
        return None

    pprint(vars(exc))

    data = {
        'status': 'ERR',
        'error': {
            'code': exc.status_code,
            'msg': response.data['detail'],
        }
    }

    response.data = data

    return response
