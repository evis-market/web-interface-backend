from rest_framework.views import exception_handler

from app.exceptions import BAD_REQUEST_CODE, Errno
from app.response import response_err


def extract_err_data_from_exc(exc):  # noqa: CCR001
    if isinstance(exc.detail, dict) and 'detail' in exc.detail:
        return exc.detail['detail'], None

    if isinstance(exc.detail, dict):
        invalid_fields = {}
        for field, detail in exc.detail.items():
            if isinstance(detail, dict):
                if isinstance(detail, dict):
                    index_details = {}
                    invalid_fields.update({field: index_details})
                    for index, details in detail.items():
                        index_details.update({index: values[0] for values in details.values()})
                else:
                    invalid_fields[field] = detail
            elif isinstance(detail, list):
                if isinstance(detail[0], dict):
                    field_details = {}
                    invalid_fields.update({field: field_details})
                    for index, item in enumerate(detail, 0):
                        if not item:
                            continue
                        field_details.update({index: values[0] for values in item.values()})
                else:
                    invalid_fields[field] = ', '.join(detail)
        return 'bad request', invalid_fields

    if isinstance(exc.detail, list):
        return ', '.join(exc.detail), None

    if isinstance(exc.detail, str) and 'Authentication' in exc.detail:
        return 'unauthorized', None

    return exc.detail, None


def default_exception_handler(exc, context):
    if issubclass(type(exc), Errno) or isinstance(exc, Errno):
        return response_err(exc.code, msg=exc.msg, invalid_fields=exc.invalid_fields, http_code=exc.http_code)

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
