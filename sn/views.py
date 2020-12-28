import requests as r
import json
import clearbit
import jwt
import datetime
from sn import config
from sn import models
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import ObjectDoesNotExist
from sn import functions


def index(request):
    def default(o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
    list_posts = list(models.Post.objects.all().values())
    return HttpResponse(json.dumps({'data': {'posts': list(list_posts)}}, sort_keys=True, indent=1, default=default))


@csrf_exempt
def signup(request):
    try:
        assert request.method == 'POST'
        title_body_dict = functions.get_dict_request(request)
        assert 'email' in title_body_dict.keys()
        assert 'company' in title_body_dict.keys()
        hunter_io_verifier = r.get('https://api.hunter.io/v2/email-verifier?email={}&api_key={}'
                                   .format(title_body_dict['email'], config.HUNTER_IO_API_KEY))
        assert hunter_io_verifier.status_code == 200
        hunter_io_verifier_json = hunter_io_verifier.json()
        assert hunter_io_verifier_json['data']['status'] in config.VALID_HUNTER_STATUSES
        clearbit.key = config.CLEARBIT_API_KEY
        clearbit_json = json.dumps({})
        clearbit_request = clearbit.Enrichment.find(email=title_body_dict['email'], company=title_body_dict['company'])
        if clearbit_request is not None:
            clearbit_json = json.dumps(clearbit_request)
        models.User.objects.create(user_name=title_body_dict['name'],
                                   user_mail=title_body_dict['email'],
                                   user_company=title_body_dict['company'],
                                   user_password=title_body_dict['password'],
                                   user_hunter_io=str(hunter_io_verifier_json),
                                   user_clearbit_com=str(clearbit_json),
                                   user_online=True)
        user_dict = models.User.objects.get(user_name=title_body_dict['name'],
                                            user_mail=title_body_dict['email'],
                                            user_company=title_body_dict['company'],
                                            user_password=title_body_dict['password'],
                                            user_hunter_io=str(hunter_io_verifier_json),
                                            user_clearbit_com=str(clearbit_json),
                                            user_online=True).__dict__
        del user_dict['_state']
        private_key = open(config.PRIVATE_KEY_RS_256, 'rb').read()
        encoded_user_data = jwt.encode(user_dict, private_key, algorithm='RS256')
        return HttpResponse(json.dumps({'data': {'encoded_user_data': encoded_user_data}}))  # Does it return right key?
    except AssertionError:
        return HttpResponse(json.dumps({'data': {'error': 'Either mail, or some request data is wrong'}}))
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'data': {'error': 'Either mail, or some request data is wrong or some '
                                                          'characters is not valid in your mail, name'}}))


@csrf_exempt
def login(request):
    try:
        assert request.method == 'GET'
        title_body_dict = functions.get_dict_request(request)
        assert 'email' in title_body_dict.keys()
        assert 'password' in title_body_dict.keys()
        user = models.User.objects.get(user_password=title_body_dict['password'],
                                       user_mail=title_body_dict['email'])
        assert user.user_online is False
        user.user_online = True
        user.save()
        user_dict = user.__dict__
        del user_dict['_state']
        private_key = open(config.PRIVATE_KEY_RS_256, 'rb').read()
        encoded_user_data = jwt.encode(user_dict, private_key, algorithm='RS256')
        return HttpResponse(json.dumps({'data': {'encoded_user_data': encoded_user_data,
                                                 'user': {'email': user_dict['user_mail']}, 'action': 'login'}}))
    except AssertionError:
        return HttpResponse(json.dumps({'data': {'error': 'User has already been authorized'}}))
    except ObjectDoesNotExist:
        return HttpResponse(
            json.dumps({'data': {'error': 'User hasn\'t been found'}}))


@csrf_exempt
def create_post(request):
    try:
        assert request.method == 'POST'
        title_body_dict = functions.get_dict_request(request)
        public_key = open(config.PUBLIC_KEY_RS_256, 'rb').read()
        assert 'encoded_user_data' in title_body_dict.keys()
        decoded_user_data = jwt.decode(title_body_dict['encoded_user_data'], public_key, algorithms='RS256')
        assert decoded_user_data['user_online'] is True
        assert 'id' in decoded_user_data.keys()
        assert 'title' in title_body_dict.keys()
        assert 'text' in title_body_dict.keys()
        models.Post.objects.create(post_likes=0,
                                   post_user_id=decoded_user_data['id'],
                                   post_title=title_body_dict['title'],
                                   post_text=title_body_dict['text'],
                                   post_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
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
        assert decoded_user_data['id'] != post.post_user_id
        try:
            models.LikedPost.objects.get(liked_post_post_id=post.id,
                                         liked_post_user_id=decoded_user_data['id'])
            return HttpResponse(json.dumps({'data': {'error': 'It seems, that is post that you want to '
                                                              'like has already been liked by you',
                                                     'success': False}}))
        except ObjectDoesNotExist:
            pass
        post = models.Post.objects.get(id=post.id)
        post.post_likes = post.post_likes + 1
        post.save()
        models.LikedPost.objects.create(liked_post_post_id=post.id, liked_post_user_id=decoded_user_data['id'])
        return HttpResponse(json.dumps({'data': {'post': post.post_title, 'action': 'like', 'success': True}}))
    except AssertionError:
        return HttpResponse(json.dumps({'data': {'error': 'It seems, that is your post, '
                                                          'you can\'t add like to your own post',
                                                 'success': False}}))
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'data': {'error': 'It seems, that is post that you want to '
                                                          'like does not exist, please, try it again',
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
        assert decoded_user_data['id'] != post.post_user_id
        try:
            models.LikedPost.objects.get(liked_post_post_id=post.id,
                                         liked_post_user_id=decoded_user_data['id'])

        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'data': {'error': 'It seems, that is post that you want to '
                                                              'like has already been disliked by you',
                                                     'success': False}}))
        post.post_likes = post.post_likes - 1
        post.save()
        models.LikedPost.objects.get(liked_post_post_id=post.id,
                                     liked_post_user_id=decoded_user_data['id']).delete()
        return HttpResponse(json.dumps({'data': {'post': post.post_title, 'action': 'dislike', 'success': True}}))
    except AssertionError:
        return HttpResponse(json.dumps({'data': {'error': 'It seems, that is your post, '
                                                          'you can\'t add dislike to your own post',
                                                 'success': False}}))
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'data': {'error': 'It seems, that is post that you want to '
                                                          'dislike does not exist, please, try it again',
                                                 'success': False}}))


@csrf_exempt
def logout(request):
    try:
        assert request.method == 'GET'
        title_body_dict = functions.get_dict_request(request)
        assert 'encoded_user_data' in title_body_dict.keys()
        public_key = open(config.PUBLIC_KEY_RS_256, 'rb').read()
        decoded_user_data = jwt.decode(title_body_dict['encoded_user_data'], public_key, algorithms='RS256')
        user = models.User.objects.get(user_password=decoded_user_data['user_password'],
                                       user_mail=decoded_user_data['user_mail'])
        assert user.user_online is True
        user.user_online = False
        user.save()
        return HttpResponse(json.dumps({'data': {'user': {'email': decoded_user_data['user_mail']}, 'action': 'logout',
                                                 'success': True}}))
    except AssertionError:
        return HttpResponse(json.dumps({'data': {'error': 'User has already been authorized'}}))
    except ObjectDoesNotExist:
        return HttpResponse(
            json.dumps({'data': {'error': 'User hasn\'t been found'}}))

# TODO What does django.model.objects.get return if there aren't any objects that is matches!!!
# TODO Check everything again before writes bot
# TODO Check rules in test task
