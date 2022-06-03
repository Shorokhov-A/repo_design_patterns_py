from framework.wsgi import Framework
from urls import url_patterns
from framework.patterns.structural_patterns import AddRoute

app = Framework(AddRoute.get_routes())
