class Request:
    def __init__(self, environ):
        self.headers = self._get_http_headers(environ)
        self.path = environ['PATH_INFO']
        self.query_params = self._get_query_params(environ)
        self.method = environ['REQUEST_METHOD'].lower()

    def _get_http_headers(self, environ):
        headers = {}
        for key, value in environ.items():
            if key.startswith('HTTP'):
                headers[key[5:]] = value
        return headers

    def _get_query_params(self, environ):
        query_params = {}
        data = environ['QUERY_STRING'].split('&')
        for el in data:
            if el:
                key, value = el.split('=')
                if query_params.get(key):
                    query_params[key].append(value)
                else:
                    query_params[key] = [value]

        return query_params
