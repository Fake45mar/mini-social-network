import hashlib
import logging as logger
from sn.tests.test_get import GetRequest
from sn.tests.test_post import PostRequest
from sn.tests import config
from random import randint, shuffle

logger.basicConfig(level=logger.INFO, filename='log/logout.log')


def main():
    url = config.requests['logout']
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
    for name, email in zip(names[:config.USER_SIGNUP], emails):
        password = ''.join([config.PASSWORD_RANDOM_CHARACTERS[randint(0, len(config.PASSWORD_RANDOM_CHARACTERS) - 1)]
                            for x in range(0, 9, 1)])
        encoded_user_data = post_request.right_event({'email': email,
                                  'password': hashlib.md5(
                                      password.encode('utf-8')).hexdigest(),
                                  'company': config.COMPANY,
                                  'name': name})['data']['encoded_user_data']
        logger.info('right event: {}'.format(get_request.right_event({'encoded_user_data': encoded_user_data})))
        logger.info('wrong event: {}'.format(get_request.wrong_event({'encoded_user_data': encoded_user_data})))


if __name__ == "__main__":
    main()
