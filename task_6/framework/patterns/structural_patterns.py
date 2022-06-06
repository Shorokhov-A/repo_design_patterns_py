import inspect
from time import time

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


class DebugMethod:

    def __call__(self, cls):
        def decorate(func):
            def new_func(self, *args, **kwargs):
                time_start = time()
                result = func(self, *args, **kwargs)
                print(f'Из {self.__name__} вызвана функция {func.__name__}'
                      f'\nВремя выполнения функции {time() - time_start}')
                return result

            return new_func

        for key, value in cls.__dict__.items():
            if inspect.isfunction(value):
                setattr(cls, key, decorate(getattr(cls, key)))
        return cls


def debug(cls):
    def decorate(func):
        def new_func(self, *args, **kwargs):
            time_start = time()
            result = func(self, *args, **kwargs)
            print(f'Из {self.__name__} вызвана функция {func.__name__}'
                  f'\nВремя выполнения функции {time() - time_start}')
            return result
        return new_func

    for key, value in cls.__dict__.items():
        if inspect.isfunction(value):
            setattr(cls, key, decorate(getattr(cls, key)))
    return cls
