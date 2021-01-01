from random import shuffle
NUMBER_OF_USERS = 10
MAX_POSTS_PER_USER = 5
MAX_LIKES_PER_USER = 5
SIGNUP_USERS = 10
FIRST_NAMES = [x.replace('\n', '') for x in open('../examples_names/NameDatabases/NamesDatabases/first_names/us.txt',
                                                 'r').readlines()]
LAST_NAMES = [x.replace('\n', '') for x in open('../examples_names/NameDatabases/NamesDatabases/surnames/us.txt',
                                                'r').readlines()]
shuffle(FIRST_NAMES)
shuffle(LAST_NAMES)
COMPANY = 'unboltsoft'
MAIL = "@gmail.com"
PASSWORD_RANDOM_CHARACTERS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

