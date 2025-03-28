# -*- coding: utf-8 -*-
from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest

from a3exception.errors import ValidationError


def load_bearer_token(request: HttpRequest):
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    prefix = "Bearer "
    try:
        token = auth_header.split(prefix)[1]
    except IndexError:
        raise ValidationError(_("Invalid authorization header."))

    request.token = token
