from rest_framework.views import exception_handler

from app.exceptions import Errno, BAD_REQUEST_CODE
from app.response import response_err


def extract_err_data_from_exc(exc):
    if isinstance(exc.detail, dict) and 'detail' in exc.detail:
        return exc.detail['detail'], None

    if isinstance(exc.detail, dict):
        invalid_fields = {}
        for field in exc.detail:
            invalid_fields[field] = ', '.join(exc.detail[field])
        return 'bad request', invalid_fields

    if isinstance(exc.detail, list):
        return ', '.join(exc.detail), None

    return exc.detail, None


def default_exception_handler(exc, context):
    if issubclass(type(exc), Errno) or isinstance(exc, Errno):
        return response_err(exc.code, exc.msg, http_code=exc.http_code)

    if issubclass(type(exc), ValueError) or isinstance(exc, ValueError):
        return response_err(BAD_REQUEST_CODE, str(exc), http_code=BAD_REQUEST_CODE)

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:
        return None

    msg, invalid_fields = extract_err_data_from_exc(exc)
    response.data = {
        'status': 'ERR',
        'error': {
            'code': exc.status_code or 500,
            'msg': msg or 'unexpected error',
        },
    }

    if invalid_fields:
        response.data['error']['invalid_fields'] = invalid_fields

    return response
