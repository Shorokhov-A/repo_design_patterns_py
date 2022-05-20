from framework.request import Request
from framework.view import View


class Framework:

    def __init__(self, urls):
        self.urls = urls

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        request = Request(environ)
        view = self._get_view(request)
        print(request.query_params)
        print(self._get_response(request, view))
        return [b'Hello world from a simple WSGI application!']

    def _get_view(self, request):
        path = request.path
        for url in self.urls:
            if url.url == path:
                return url.view

    def _get_response(self, request: Request, view: View):
        if hasattr(view, request.method):
            return getattr(view, request.method)(view, request)
        else:
            return 'Метод недоступен.'
