import hashlib
import requests as r
import json


class User:
    def __init__(self, name: str, email: str, password: str, company: str):
        self.name = name
        self.email = email
        self._password = password
        self.company = company
        self._encoded_user_data = ''
        self.likes = 0
        self.posts = 0

    def signup(self) -> json:
        url = 'http://127.0.0.1:8000/signup'
        hashed_password = hashlib.md5(self._password.encode('utf-8')).hexdigest()
        data = {
            'email': self.email,
            'password': hashed_password,
            'company': self.company,
            'name': self.name
        }
        request = r.post(url, data=data)
        request_json = request.json()
        assert 'data' in request_json.keys()
        assert 'encoded_user_data' in request_json['data'].keys()
        self._encoded_user_data = request_json['data']['encoded_user_data']
        return request_json

    def login(self) -> json:
        url = 'http://127.0.0.1:8000/login'
        hashed_password = hashlib.md5(self._password.encode('utf-8')).hexdigest()
        data = {
            'email': self.email,
            'password': hashed_password
        }
        request = r.get(url, data=data)
        request_json = request.json()
        assert 'data' in request_json.keys()
        assert 'encoded_user_data' in request_json['data'].keys()
        self._encoded_user_data = request_json['data']['encoded_user_data']
        return request_json

    def logout(self) -> json:
        url = 'http://127.0.0.1:8000/logout'
        data = {
            'encoded_user_data': self._encoded_user_data
        }
        request = r.get(url, data=data)
        request_json = request.json()
        return request_json

    def like(self, post_title: str) -> json:
        url = 'http://127.0.0.1:8000/like'
        data = {
            'encoded_user_data': self._encoded_user_data,
            'title': post_title
        }
        request = r.get(url, data=data)
        request_json = request.json()
        self.likes += 1
        return request_json

    def dislike(self, post_title: str) -> json:
        url = 'http://127.0.0.1:8000/dislike'
        data = {
            'encoded_user_data': self._encoded_user_data,
            'title': post_title
        }
        request = r.get(url, data=data)
        request_json = request.json()
        self.likes -= 1
        return request_json

    def create_post(self, post_title, post_text):
        url = 'http://127.0.0.1:8000/create_post'
        data = {
            'encoded_user_data': self._encoded_user_data,
            'title': post_title,
            'text': post_text
        }
        request = r.post(url, data=data)
        request_json = request.json()
        self.posts += 1
        return request_json
