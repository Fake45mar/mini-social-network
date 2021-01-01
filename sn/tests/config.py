url = 'http://127.0.0.1:8000/'
requests = {
    'signup': url + 'signup',
    'login': url + 'login',
    'create_post': url + 'create_post',
    'like': url + 'like',
    'dislike': url + 'dislike',
    'logout': url + 'logout'
}
USER_SIGNUP = 10
COMPANY = 'unboltsoft'
MAIL = "@gmail.com"
PASSWORD_RANDOM_CHARACTERS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMBER_OF_USERS = 10
MAX_POSTS_PER_USER = 5
MAX_LIKES_PER_USER = 5
FIRST_NAMES = [x.replace('\n', '') for x in
               open('../../examples_names/NameDatabases/NamesDatabases/first_names/us.txt', 'r').readlines()]
LAST_NAMES = [x.replace('\n', '') for x in
              open('../../examples_names/NameDatabases/NamesDatabases/surnames/us.txt', 'r').readlines()]
