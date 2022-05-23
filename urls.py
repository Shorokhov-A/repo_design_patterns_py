from framework.url import Url
from views import Homepage, AboutPage, Contacts

url_patterns = [
    Url('/', Homepage),
    Url('/about/', AboutPage),
    Url('/contacts/', Contacts),
]
