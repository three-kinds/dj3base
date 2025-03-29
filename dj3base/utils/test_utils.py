# -*- coding: utf-8 -*-
import sys
import json
from tempfile import NamedTemporaryFile
from typing import IO
from a3exception.dynamic_error_factory import DynamicErrorFactory
from django.test.client import Client


_IS_UNIT_TESTING = sys.argv[1:2] == ["test"]


def is_unit_testing() -> bool:
    return _IS_UNIT_TESTING


def post_json_return_json(client: Client, path: str, data: dict | None = None) -> dict:
    response = client.post(path=path, data=json.dumps(data), content_type="application/json")
    rd = response.json()
    if response.status_code == 200:
        return rd
    else:
        raise DynamicErrorFactory.build_error_by_status(**rd)


def post_json_return_file(
    client: Client, path: str, data: dict | None = None, need_delete_file: bool = True, **kwargs
) -> IO:
    response = client.post(path=path, data=json.dumps(data), content_type="application/json")
    tf = NamedTemporaryFile("wb", delete=need_delete_file, **kwargs)
    for content in response.streaming_content:
        tf.write(content)
    tf.flush()
    return tf
