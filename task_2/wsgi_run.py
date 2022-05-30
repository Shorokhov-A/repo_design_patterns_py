from framework.wsgi import Framework
from urls import url_patterns

app = Framework(url_patterns)
