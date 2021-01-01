import hashlib
import requests as r
import logging as logger
from sn.tests.test_get import GetRequest
from sn.tests.test_post import PostRequest
from sn.tests import config
from random import randint, shuffle

logger.basicConfig(level=logger.INFO, filename='log/dislike.log')


def main():
    url = config.requests['dislike']
    get_request = GetRequest(url)
    post_request = PostRequest(config.requests['signup'])
    first_names = config.FIRST_NAMES
    surnames = config.LAST_NAMES
    shuffle(first_names)
    shuffle(surnames)
    assert len(first_names) > config.USER_SIGNUP
    assert len(surnames) > config.USER_SIGNUP
    names = [x + " " + y for x, y in zip(first_names[:config.USER_SIGNUP], surnames[:config.USER_SIGNUP])]
    emails = [x.replace(" ", "") + config.MAIL for x in names]
    posts = r.get(config.url).json()['data']['posts']
    for name, email in zip(names[:config.USER_SIGNUP], emails):
        password = ''.join([config.PASSWORD_RANDOM_CHARACTERS[randint(0, len(config.PASSWORD_RANDOM_CHARACTERS) - 1)]
                            for x in range(0, 9, 1)])
        encoded_user_data = post_request.right_event({'email': email,
                                                      'password': hashlib.md5(
                                                          password.encode('utf-8')).hexdigest(),
                                                      'company': config.COMPANY,
                                                      'name': name})['data']['encoded_user_data']
        posts_per_user = []
        PostRequest(config.requests['create_post']).right_event({'encoded_user_data': encoded_user_data,
                                                                 'title': name, 'text': password})
        posts_per_user.append({'post_title': name})

        PostRequest(config.requests['create_post']).right_event({'encoded_user_data': encoded_user_data,
                                                                 'title': password, 'text': name})
        posts_per_user.append({'post_title': password})

        PostRequest(config.requests['create_post']).right_event({'encoded_user_data': encoded_user_data,
                                                                 'title': name + password, 'text': password})
        posts_per_user.append({'post_title': name + password})

        for post in posts[:config.MAX_LIKES_PER_USER]:
            print(post)
            logger.info('right event: {}'.format(get_request.right_event({'encoded_user_data': encoded_user_data,
                                                                          'title': post['post_title']})))
        for post in posts_per_user:
            logger.info('wrong event: {}'.format(get_request.wrong_event({'encoded_user_data': encoded_user_data,
                                                                          'title': post['post_title']})))


if __name__ == "__main__":
    main()
