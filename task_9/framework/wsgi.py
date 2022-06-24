from framework.request import Request
from framework.view import View

from pprint import pprint


class Framework:

    def __init__(self, urls):
        self.urls = urls

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        request = Request(environ)
        view = self._get_view(request)
        print(request.query_params)
        print(self._get_response(request, view))
        return [view.get_template(view).encode(encoding='utf-8') if view else b'Page not found']

    def _get_view(self, request):
        path = self._get_path(request.path)
        for url in self.urls:
            if url.url == path:
                return url.view

    def _get_response(self, request: Request, view: View):
        if hasattr(view, request.method):
            return getattr(view, request.method)(view, request)
        else:
            return 'Метод недоступен.'

    def _get_path(self, path):
        if not path.endswith('/'):
            path = ''.join((path, '/'))
        return path


class FakeFramework(Framework):
    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
