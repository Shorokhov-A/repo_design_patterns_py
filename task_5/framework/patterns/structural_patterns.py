from framework.url import Url


class AddRoute:
    routes = []

    def __init__(self, url):
        self.url = url

    def __call__(self, cls):
        self.routes.append(Url(self.url, cls))

    @classmethod
    def get_routes(cls):
        return cls.routes
