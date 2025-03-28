# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import JsonResponse
from a3exception.errors import Error, ErrorType


def build_success_response(data: dict = None):
    success_result = {"status": "OK"}

    if data is not None:
        success_result["data"] = data
    return JsonResponse(data=success_result)


def build_error_response(e: Error) -> JsonResponse:
    status_code = getattr(settings, "CLIENT_SIDE_ERROR_STATU_SCODE", 499)
    if e.error_type == ErrorType.ServerSideError:
        status_code = getattr(settings, "SERVER_SIDE_ERROR_STATU_SCODE", 599)

    rd = {"status": e.status, "message": e.message}
    if e.detail is not None:
        rd["detail"] = e.detail

    return JsonResponse(data=rd, status=status_code)
