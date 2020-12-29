import logging as logger
import requests as r
from bot_tester import config
from bot_tester.User import User
from random import seed, randint, gauss
from datetime import datetime
logger.basicConfig(filename='bot.log', level=logger.INFO)
seed(1)

if __name__ == "__main__":
    list_users = []
    # initialize users
    for i in range(0, config.NUMBER_OF_USERS, 1):
        name_random = randint(0, len(config.FIRST_NAMES))
        surname_random = randint(0, len(config.LAST_NAMES))
        full_name = config.FIRST_NAMES[name_random] + " " + config.LAST_NAMES[surname_random]
        email = full_name.replace(" ", "") + config.MAIL
        password = ''.join([config.PASSWORD_RANDOM_CHARACTERS[randint(0, len(config.PASSWORD_RANDOM_CHARACTERS) - 1)]
                            for x in range(0, 9, 1)])
        logger.info('full_name: {}'.format(full_name))
        logger.info('email: {}'.format(email))
        logger.info('password: {}'.format(password))
        logger.info('\n')
        list_users.append(User(
            full_name,
            email,
            password,
            config.COMPANY
        ))
    # signup users
    list_json_signups = []
    for user in list_users:
        signup = user.signup()
        list_json_signups.append(signup)
    logger.info('list of signup_json: {}'.format(list_json_signups))
    # if user is signed up, he is already authorized
    # login
    list_json_login = []
    for user in list_users:
        try:
            login = user.login()
            list_json_login.append(login)
        except AssertionError:
            pass
    # create posts
    list_json_create_posts = []
    user_posts = {}
    for user in list_users:
        user_posts[user] = []
        for num in range(0, randint(0, config.MAX_POSTS_PER_USER), 1):
            create_post = user.create_post(user.name + ' title {} {}'.format(len(user.name), gauss(0, 1)),
                                           user.name*2 + user.email*2 + user.company*2 +
                                           datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            user_posts[user].append(create_post['data']['post'])
    logger.info('list_json_create_posts: {}'.format(list_json_create_posts))
    posts = r.get('http://127.0.0.1:8000/')
    # likes
    list_json_like_dislike = []
    user_sort = {}
    for user in list_users:
        user_sort[user.posts] = user
    user_sort_keys = list(user_sort.keys())
    user_sort_keys.sort(reverse=True)
    for user_key in user_sort_keys:
        user = user_sort[user_key]
        for user_posts_key in user_posts.keys():
            posts = user_posts[user_posts_key]
            for post in posts:
                if user.likes <= config.MAX_LIKES_PER_USER:
                    if randint(0, 1) == 0:
                        json_likes = user.like(post)
                        list_json_like_dislike.append(json_likes)
                    else:
                        json_dislikes = user.like(post)
                        list_json_like_dislike.append(json_dislikes)
                else:
                    break
    logger.info('list_json_like_dislike: {}'.format(list_json_like_dislike))
    for user in list_users:
        user.logout()
    logger.info('All users are logout')
