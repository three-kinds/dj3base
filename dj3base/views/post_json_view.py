# -*- coding: utf-8 -*-
import abc
import json
from typing import Any, Type, Optional
import inspect

from django.views.generic import View
from django.http import FileResponse
from django.utils.translation import gettext_lazy as _
from a3exception.errors import ServerKnownError, ValidationError
from dj3base.utils.response_utils import build_success_response
from a3json_struct.struct import JsonStruct
from a3json_struct.errors import ValidationError as StructValidationError


class PostJsonView(View):
    request_struct_cls: Type[JsonStruct]

    def _get_request_json_data(self) -> dict:
        try:
            return json.loads(self.request.body)
        except Exception as e:
            raise ValidationError(_("The request body is not a valid JSON."), cause=str(e))

    def validate_request_permission(self):
        pass

    def validate_request_struct(self) -> Optional[JsonStruct]:
        request_struct = None

        request_struct_cls = getattr(self, "request_struct_cls", None)
        if request_struct_cls is not None and inspect.isclass(request_struct_cls):
            data = self._get_request_json_data()
            request_struct = request_struct_cls(**data)
            try:
                request_struct.full_clean()
            except StructValidationError as e:
                raise ValidationError(str(e))

        return request_struct

    def post(self, *_, **__):
        self.validate_request_permission()
        request_struct = self.validate_request_struct()
        custom_params = self.custom_validate(request_struct)

        result = self.handle_post(request_struct, custom_params)
        if result is None:
            return build_success_response()
        elif isinstance(result, dict):
            return build_success_response(result)
        elif isinstance(result, FileResponse):
            return result
        else:
            raise ServerKnownError(cause=f"The return type of handle_post is unknown: {type(result).__name__}")

    def custom_validate(self, request_struct) -> Any:
        pass

    @abc.abstractmethod
    def handle_post(self, request_struct, custom_params: dict):
        raise NotImplementedError()
