class AbstractTestApi:
    def __init__(self, url):
        self._url = url

    @classmethod
    def right_event(cls, data):
        pass

    @classmethod
    def wrong_event(cls, data):
        pass
