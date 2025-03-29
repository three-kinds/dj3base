import os.path

from django.http import FileResponse
from a3exception import errors
from a3json_struct import struct

from dj3base.views import PostJsonView


class RequestStruct(struct.JsonStruct):
    message: str = struct.CharField(min_length=1, max_length=10)


class EchoView(PostJsonView):
    request_struct_cls = RequestStruct

    def handle_post(self, request_struct: RequestStruct, custom_params: dict):
        if request_struct.message == "error":
            raise errors.ForbiddenError(f"Message can not be 'error'.")
        return {"message": request_struct.message}


class FileResponseView(PostJsonView):
    def handle_post(self, request_struct: RequestStruct, custom_params: dict):
        base_dir = os.path.dirname(__file__)
        return FileResponse(open(os.path.join(base_dir, "views.py"), "rb"))


class EmptyView(PostJsonView):
    def handle_post(self, request_struct: RequestStruct, custom_params: dict):
        return
