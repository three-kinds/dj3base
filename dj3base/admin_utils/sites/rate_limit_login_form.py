# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class RateLimitLoginForm(AuthenticationForm):

    def clean(self):
        # 检测IP异常数是否达到上限，如果受限，直接抛出相关异常
        raise ValidationError(
            "登录的次数已达上限，请1天后重试！",
            code="invalid_login",
        )

        try:
            return super().clean()
        except ValidationError as e:
            # IP 异常数 + 1
            raise e
