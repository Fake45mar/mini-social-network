from sn.tests.test_post import PostRequest
from sn.tests import config


def main():
    url = config.requests['signup']
    post_request = PostRequest(url)


if __name__ == "__main__":
    main()
