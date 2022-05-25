from framework.url import Url
from views import Homepage, AboutPage

url_patterns = [
    Url('/', Homepage),
    Url('/about/', AboutPage)
]
