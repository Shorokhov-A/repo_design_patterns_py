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


class CreateCategory(View):

    template_name = 'create_category.html'

    def get(self, request):
        with open('categories.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f)
        with open('categories.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        return 'GET SUCCESS'

    def post(self, request):
        data = self.data
        if data.get('category'):
            data['category'].extend(request.data['category'])
        else:
            data['category'] = request.data['category']
        with open('categories.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f)
        return 'POST SUCCESS'
