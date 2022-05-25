import urllib.parse


class Request:
    def __init__(self, environ):
        self.headers = self._get_http_headers(environ)
        self.path = environ['PATH_INFO']
        self.query_params = self._get_query_params(environ)
        self.method = environ['REQUEST_METHOD'].lower()
        self.data = self._get_wsgi_input_data(environ)

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

    def _parse_input_data(self, data: str):
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                key, value = item.split('=')
                result[key] = value

        return result

    def _get_wsgi_input_data(self, environ):
        result = {}
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        if data:
            data_string = data.decode(encoding='utf-8').replace('+', ' ')
            data_string = urllib.parse.unquote(data_string)
            result = self._parse_input_data(data_string)
        return result
