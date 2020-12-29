INPUT_DATA = [x.replace('\n', '') for x in open('./input_data', 'r').readlines()]
NUMBER_OF_USERS = 10
MAX_POSTS_PER_USER = 5
MAX_LIKES_PER_USER = 5
SIGNUP_USERS = 10
FIRST_NAMES = [x.replace('\n', '') for x in open('../examples_names/NameDatabases/NamesDatabases/first names/all.txt',
                                                 'r').readlines()]
LAST_NAMES = [x.replace('\n', '') for x in open('../examples_names/NameDatabases/NamesDatabases/surnames/all.txt',
                                                'r').readlines()]
COMPANY = 'unboltsoft'
MAIL = "@gmail.com"
PASSWORD_RANDOM_CHARACTERS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
if __name__ == "__main__":
    print(INPUT_DATA)
