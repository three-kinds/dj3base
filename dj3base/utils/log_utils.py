# -*- coding: utf-8 -*-
import logging
import traceback

from django.http import HttpRequest
from a3exception.errors import Error, ErrorType

from dj3base.utils import request_utils as ru


def log_error_message(logger: logging.Logger, request: HttpRequest, e: Error) -> str:
    if e.error_type == ErrorType.ServerSideError:
        error_message = f"\n" \
           f"ip: {ru.get_ip(request)}\n" + \
           f"url: {ru.get_full_url(request)}\n" + \
           f"content-type: {request.content_type}\n" + \
           f"request: {ru.get_request_data(request)}\n" + \
           f"message: {e.message}\n" + \
           f"cause: {e.cause}\n" + \
           f"traceback: {traceback.format_exc()}\n"
        logger.critical(error_message)
    else:
        error_message = f'[{request.path}]-[{e.status}]: {e.message}; {e.cause or ""}'
        logger.info(error_message)

    return error_message
