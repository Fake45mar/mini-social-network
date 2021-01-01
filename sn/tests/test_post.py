import  requests as r
from sn.tests.abstract_test import AbstractTestApi


class PostRequest(AbstractTestApi):
    def __init__(self, url):
        super().__init__(url)

    def right_event(self, data):
        request = r.post(self._url, data=data)
        assert 'encoded_user_data' in request.json()['data'].keys()
        return request.json()

    def wrong_event(self, data):
        request = r.post(self._url, data=data)
        print(request.json())
        assert 'error' in request.json()['data'].keys()
        return request.json()
