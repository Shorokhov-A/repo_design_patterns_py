import inspect
import types

from framework.url import Url


class AddRoute:
    routes = []

    def __init__(self, url):
        self.url = url

    def __call__(self, cls):
        self.routes.append(Url(self.url, cls))
        return cls

    @classmethod
    def get_routes(cls):
        return cls.routes


# class DebugMethod:
#
#     def __call__(self, cls):
#         for key, value in cls.__dict__.items():
#             if inspect.isfunction(value):
#                 print(key)


def debug(cls):
    def decorate(func):
        def new_func(self, request):
            print(f'Из {self.__name__} вызвана функция {func.__name__}')
            return func(self, request)
        return new_func

    for key, value in cls.__dict__.items():
        if inspect.isfunction(value):
            setattr(cls, key, decorate(getattr(cls, key)))
    return cls
