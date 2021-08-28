from rest_framework.views import exception_handler

from app.exceptions import Errno
from app.response import response_err


def default_exception_handler(exc, context):
    if issubclass(type(exc), Errno) or isinstance(exc, Errno):
        return response_err(exc.code, exc.msg, http_code=exc.http_code)

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:
        return None

    data = {
        'status': 'ERR',
        'error': {
            'code': exc.status_code or 500,
            'msg': 'unexpected error',
        },
    }

    if isinstance(exc.detail, dict):
        data['error']['msg'] = 'bad request'
        data['error']['invalid_fields'] = {}
        for field in exc.detail:
            data['error']['invalid_fields'][field] = ', '.join(exc.detail[field])

    elif isinstance(exc.detail, list):
        data['error']['msg'] = ', '.join(exc.detail)
    else:
        data['error']['msg'] = exc.detail

    response.data = data

    return response
