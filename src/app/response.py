from rest_framework.response import Response


def response_ok(data, http_code=None, template_name=None, headers=None, content_type=None):
    if not data:
        data = {}

    data['status'] = 'OK'
    return Response(data, status=http_code, template_name=template_name, headers=headers, content_type=content_type)


def response_err(code: int, msg: str, http_code=None, template_name=None, headers=None, content_type=None):
    data = {
        'status': 'ERR',
        'error': {
            'code': http_code or 500,
            'msg': 'unexpected error',
        },
    }

    if code:
        data['error']['code'] = code

    if msg:
        data['error']['msg'] = msg

    return Response(data, status=http_code, template_name=template_name, headers=headers, content_type=content_type)
