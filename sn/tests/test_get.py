import requests as r
from sn.tests.abstract_test import AbstractTestApi


class GetRequest(AbstractTestApi):
    def __init__(self, url):
        super().__init__(url)

    def right_event(self, data):
        request = r.get(self._url, data=data)
        assert 'encoded_user_data' in request.json().keys()

    def wrong_event(self, data):
        request = r.get(self._url, data=data)
        assert 'Error' in request.json().keys()