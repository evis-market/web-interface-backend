from rest_framework.views import exception_handler

from app.exceptions import BAD_REQUEST_CODE, Errno
from app.response import response_err


def extract_err_data_from_exc(exc):
    if isinstance(exc.detail, dict) and 'detail' in exc.detail:
        return exc.detail['detail'], None

    if isinstance(exc.detail, dict):
        invalid_fields = {}
        for field, detail in exc.detail.items():
            if isinstance(detail, dict):
                invalid_fields[field] = detail
            elif isinstance(detail, list):
                if isinstance(detail[0], dict):
                    for item in detail:
                        if not item:
                            continue
                        invalid_fields.update({k: v for k, v in item.items()})
                else:
                    invalid_fields[field] = ', '.join(detail)
        return 'bad request', invalid_fields

    if isinstance(exc.detail, list):
        return ', '.join(exc.detail), None

    return exc.detail, None


    # if isinstance(exc.detail, dict):
    #     invalid_fields = {}
    #     for field, detail in exc.detail.items():
    #         if isinstance(detail, list):
    #             for field_errordict in detail:
    #                 if field_errordict:
    #                     invalid_fields[list(field_errordict.keys())[0]] = field_errordict.values()
    #         elif isinstance(detail, dict) and detail:
    #             invalid_fields[field] = detail
    #         else:
    #             invalid_fields[field] = ', '.join(detail)
    #     return 'bad request', invalid_fields



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
