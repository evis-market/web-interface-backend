from rest_framework import status


BAD_REQUEST_CODE = 400
UNAUTHORIZED_CODE = 401
FORBIDDEN_CODE = 403
NOT_FOUND = 404


class Errno(Exception):
    def __init__(self, code=None, msg=None, http_code=None):
        self.code = code or self.default_code
        self.msg = msg or self.default_msg
        self.http_code = http_code or self.default_http_code


class BadRequest(Errno):
    default_code = BAD_REQUEST_CODE
    default_msg = 'Bad request'
    default_http_code = status.HTTP_400_BAD_REQUEST


class Unauthorized(Errno):
    default_code = UNAUTHORIZED_CODE
    default_msg = 'Unauthorized'
    default_http_code = status.HTTP_401_UNAUTHORIZED


class Forbidden(Errno):
    default_code = FORBIDDEN_CODE
    default_msg = 'Forbidden'
    default_http_code = status.HTTP_403_FORBIDDEN


class NotFound(Errno):
    default_code = NOT_FOUND
    default_msg = 'Not found'
    default_http_code = status.HTTP_404_NOT_FOUND
