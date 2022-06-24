from framework.wsgi import Framework, FakeFramework
from urls import url_patterns
from framework.patterns.structural_patterns import AddRoute

app = Framework(AddRoute.get_routes())
# app = FakeFramework(AddRoute.get_routes())
