from framework.url import Url
from views import Homepage, AboutPage, Contacts, CreateCategory, CreateCourse

url_patterns = [
    Url('/', Homepage),
    Url('/about/', AboutPage),
    Url('/contacts/', Contacts),
    Url('/create_category/', CreateCategory),
    Url('/create_course/', CreateCourse),
]
