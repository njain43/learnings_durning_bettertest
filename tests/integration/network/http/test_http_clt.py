
from unittest import TestCase, skip
import json

from src.network.http import clt



@skip
class TestHttpClt(TestCase):

    def setUp(self):
        self.test_clt = clt.Http()
        self.jsn_data = {'MSFT': 12}

    def test_get_status(self):
        result = self.test_clt.get()
        self.assertEqual(200, result.status_code)

    def test_post_data(self):
        result = self.test_clt.post(self.jsn_data)
        print(result.status_code)
        print(result.text)

    def test_call_post_without_data(self):
        result = self.test_clt.post()
        print(result.status_code)
        print(result.text)

    def test_get_with_post_url(self):
        self.test_clt = clt.Http('https://ptsv3.com/t/injaxn/post/')
        result = self.test_clt.get()
        self.assertEqual(200, result.status_code)
        self.assertEqual(json.loads(result.text), self.jsn_data)
