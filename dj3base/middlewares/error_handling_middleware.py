# -*- coding: utf-8 -*-
import logging
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin
from a3exception.errors import Error, ServerUnknownError

from dj3base.utils.log_utils import log_error_message
from dj3base.utils.response_utils import build_error_response


logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(MiddlewareMixin):
    def process_exception(self, request: HttpRequest, exception: Exception):
        if isinstance(exception, Error):
            error_response = build_error_response(exception)
            log_error_message(logger, request, exception)
        else:
            exception = ServerUnknownError(cause=str(exception))
            error_response = build_error_response(exception)
            log_error_message(logger, request, exception)

        return error_response
