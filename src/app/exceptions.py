from rest_framework import status


BAD_REQUEST_CODE = 400
UNAUTHORIZED_CODE = 401
FORBIDDEN_CODE = 403
NOT_FOUND_CODE = 404
CONFLICT_CODE = 409


class Errno(Exception):
    def __init__(self, msg=None, invalid_fields=None, code=None, http_code=None):
        self.msg = msg or self.default_msg
        self.code = code or self.default_code
        self.http_code = http_code or self.default_http_code
        self.invalid_fields = invalid_fields


class BadRequest(Errno):
    default_code = BAD_REQUEST_CODE
    default_msg = 'Bad request'
    default_http_code = status.HTTP_400_BAD_REQUEST


class InvalidFields(Errno):
    default_code = BAD_REQUEST_CODE
    default_msg = 'Bad request'
    default_http_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, msg=None, code=None, http_code=None, invalid_fields=None):
        super().__init__(self, msg=msg, code=code, http_code=http_code, invalid_fields=invalid_fields)


class Unauthorized(Errno):
    default_code = UNAUTHORIZED_CODE
    default_msg = 'Unauthorized'
    default_http_code = status.HTTP_401_UNAUTHORIZED


class Forbidden(Errno):
    default_code = FORBIDDEN_CODE
    default_msg = 'Forbidden'
    default_http_code = status.HTTP_403_FORBIDDEN


class NotFound(Errno):
    default_code = NOT_FOUND_CODE
    default_msg = 'Not found'
    default_http_code = status.HTTP_404_NOT_FOUND


class Conflict(Errno):
    default_code = CONFLICT_CODE
    default_msg = 'Conflict'
    default_http_code = status.HTTP_409_CONFLICT
