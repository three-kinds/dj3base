from django.test import TestCase
from a3exception import errors
from dj3base.utils.test_utils import post_json_return_json, post_json_return_file


class TestPostJsonView(TestCase):
    def test_return_json_success(self):
        message = "hello"
        rd = post_json_return_json(self.client, "/api/echo", {"message": message})
        self.assertEqual(rd["data"]["message"], message)

    def test_return_json_failure(self):
        with self.assertRaises(errors.ValidationError):
            post_json_return_json(self.client, "/api/echo", {"message": ""})

        message = "error"
        with self.assertRaises(errors.ForbiddenError):
            post_json_return_json(self.client, "/api/echo", {"message": message})

    def test_return_file_response(self):
        tf = post_json_return_file(self.client, "/api/file")
        with open(tf.name, "r") as f:
            content = f.read()
        self.assertIn("FileResponseView", content)

    def test_empty_response(self):
        rd = post_json_return_json(self.client, "/api/empty")
        self.assertTrue('data' not in rd)
