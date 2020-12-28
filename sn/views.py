import requests as r
import json
import clearbit
import jwt
from datetime import datetime
from sn import config
from sn import models
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sn import functions


def index(request):
    list_posts = models.Post.objects.all()
    print(models.User.objects.get().__dict__)
    return HttpResponse(str(request.COOKIES))


@csrf_exempt
def signup(request):
    try:
        assert request.method == 'POST'
        title_body_dict = functions.get_dict_request(request)
        assert 'email' in title_body_dict.keys()
        assert 'company' in title_body_dict.keys()
        hunter_io_verifier = r.get('https://api.hunter.io/v2/email-verifier?email={}&api_key={}'
                                   .format(title_body_dict['email'], config.HUNTER_IO_API_KEY))
        print(hunter_io_verifier.status_code)
        assert hunter_io_verifier.status_code == 200
        hunter_io_verifier_json = hunter_io_verifier.json()
        assert hunter_io_verifier_json['data']['status'] in config.VALID_HUNTER_STATUSES
        clearbit.key = config.CLEARBIT_API_KEY
        clearbit_json = json.dumps({})
        clearbit_request = clearbit.Enrichment.find(email=title_body_dict['email'], company=title_body_dict['company'])
        if clearbit_request is not None:
            clearbit_json = json.dumps(clearbit_request)
        print(clearbit_json)
        print(title_body_dict)
        print(hunter_io_verifier)
        models.User.objects.create(user_name=title_body_dict['name'],
                                   user_mail=title_body_dict['email'],
                                   user_company=title_body_dict['company'],
                                   user_password=title_body_dict['password'],
                                   user_hunter_io=str(hunter_io_verifier_json),
                                   user_clearbit_com=str(clearbit_json),
                                   user_online=True)
        private_key = open(config.PRIVATE_KEY_RS_256, 'rb').read()
        title_body_dict['user_hunter_io'] = str(hunter_io_verifier_json)
        title_body_dict['user_clearbit_com'] = str(clearbit_json)
        title_body_dict['user_online'] = True
        encoded_user_data = jwt.encode(title_body_dict, private_key, algorithm='RS256')
        return HttpResponse(json.dumps({'data': {'encoded_user_data': encoded_user_data}}))  # Does it return right key?
    except AssertionError as e:
        return HttpResponse(json.dumps({'data': {'error': 'Either mail, or some request data is wrong'}}))


@csrf_exempt
def login(request):
    try:
        assert request.method == 'GET'
        title_body_dict = functions.get_dict_request(request)
        assert 'email' in title_body_dict.keys()
        assert 'password' in title_body_dict.keys()
        print(title_body_dict)
        print(models.User.objects.get(user_password=title_body_dict['password'],
                                      user_mail=title_body_dict['email']).__dict__)
        assert models.User.objects.get(user_password=title_body_dict['password'],
                                       user_mail=title_body_dict['email']) is not None
        assert models.User.objects.get(user_password=title_body_dict['password'],
                                       user_mail=title_body_dict['email']).user_online is False
        models.User.objects.get(user_password=title_body_dict['password'],
                                user_mail=title_body_dict['email']).user_online = True
        user = models.User.objects.get(user_password=title_body_dict['password'],
                                       user_mail=title_body_dict['email']).__dict__
        assert user is not None
        del user['_state']
        print(user)
        private_key = open(config.PRIVATE_KEY_RS_256, 'rb').read()
        encoded_user_data = jwt.encode(user, private_key, algorithm='RS256')
        return HttpResponse(json.dumps({'data': {'encoded_user_data': encoded_user_data}}))
    except AssertionError:
        return HttpResponse(json.dumps({'data': {'error': 'User has already been authorized'}}))


@csrf_exempt
def create_post(request):
    try:
        assert request.method == 'POST'
        title_body_dict = functions.get_dict_request(request)
        public_key = open(config.PUBLIC_KEY_RS_256, 'rb').read()
        assert 'encoded_user_data' in title_body_dict.keys()
        decoded_user_data = jwt.decode(title_body_dict['encoded_user_data'], public_key, algorithms='RS256')
        print(decoded_user_data)
        assert decoded_user_data['user_online'] is True
        assert 'title' in title_body_dict.keys()
        assert 'text' in title_body_dict.keys()
        models.Post.objects.create(post_likes=0,
                                   post_user_id=decoded_user_data['id'],
                                   post_title=title_body_dict['title'],
                                   post_text=title_body_dict['text'],
                                   post_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return HttpResponse(json.dumps({'data': {'post': title_body_dict['title'], 'success': True}}))
    except AssertionError:
        return HttpResponse(json.dumps({'data': {'error': 'Please, pay attention to post details'}}))


@csrf_exempt
def like(request):
    try:
        assert request.method == 'GET'
        title_body_dict = functions.get_dict_request(request)
        public_key = open(config.PUBLIC_KEY_RS_256, 'rb').read()
        assert 'encoded_user_data' in title_body_dict.keys()
        decoded_user_data = jwt.decode(title_body_dict['encoded_user_data'], public_key, algorithms='RS256')
        assert decoded_user_data['user_online'] is True
        assert 'title' in title_body_dict.keys()  # problem moment
        post = models.Post.objects.get(post_title=title_body_dict['title'])
        assert post is not None
        post_dict = post.__dict__
        del post_dict['_state']
        assert decoded_user_data['id'] != post_dict['post_user_id']
        assert models.LikedPost.objects.get(liked_post_post_id=post_dict['id'],
                                            liked_post_user_id=decoded_user_data['id']) is None
        models.Post.objects.get(id=post_dict['id']).update(post_likes=post_dict['post_likes'] + 1)
        models.LikedPost.objects.create(liked_post_post_id=post_dict['id'], liked_post_user=decoded_user_data['id'])
        return HttpResponse(json.dumps({'data': {'post': post_dict['title'], 'success': True}}))
    except AssertionError:
        return HttpResponse(json.dumps({'data': {'error': 'It seems, that is your post, '
                                                          'you can\'t add like to your own post',
                                                 'success': False}}))


@csrf_exempt
def dislike(request):
    try:
        assert request.method == 'GET'
        title_body_dict = functions.get_dict_request(request)
        public_key = open(config.PUBLIC_KEY_RS_256, 'rb').read()
        assert 'encoded_user_data' in title_body_dict.keys()
        decoded_user_data = jwt.decode(title_body_dict['encoded_user_data'], public_key, algorithms='RS256')
        assert decoded_user_data['user_online'] is True
        assert 'title' in title_body_dict.keys()  # problem moment
        post = models.Post.objects.get(post_title=title_body_dict['title'])
        assert post is not None
        post_dict = post.__dict__
        del post_dict['_state']
        assert decoded_user_data['id'] != post_dict['post_user_id']
        assert models.LikedPost.objects.get(liked_post_post_id=post_dict['id'],
                                            liked_post_user_id=decoded_user_data['id']) is not None
        models.Post.objects.get(id=post_dict['id']).update(post_likes=post_dict['post_likes'] - 1)
        models.LikedPost.objects.get(liked_post_post_id=post_dict['id'],
                                     liked_post_user=decoded_user_data['id']).delete()
        return HttpResponse(json.dumps({'data': {'post': post_dict['title'], 'success': True}}))
    except AssertionError:
        return HttpResponse(json.dumps({'data': {'error': 'It seems, that is your post, '
                                                          'you can\'t add dislike to your own post',
                                                 'success': False}}))

# TODO What does django.model.objects.get return if there aren't any objects that is matches!!!
# TODO Check everything again before writes bot
# TODO Check rules in test task
