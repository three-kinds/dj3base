# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


chinese_phone_number_validator = RegexValidator(
    r"^1[0-9]{10}$",
    message=_("Please enter a correct chinese mobile phone number."),
)
