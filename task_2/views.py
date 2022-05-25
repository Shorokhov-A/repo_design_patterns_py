import json

from framework.view import View


class Homepage(View):

    template_name = 'index.html'

    def get(self, request):
        return 'GET SUCCESS'

    def post(self, request):
        return 'POST SUCCESS'


class AboutPage(View):

    template_name = 'about.html'


class Contacts(View):

    template_name = 'contacts.html'

    def get(self, request):
        return 'GET SUCCESS'

    def post(self, request):
        with open('message.json', 'w', encoding='utf-8') as f:
            json.dump(request.data, f)
        return 'POST SUCCESS'
