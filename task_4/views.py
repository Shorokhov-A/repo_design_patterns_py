import json

from framework.view import View
from framework.patterns.generative_patterns import Engine

site = Engine()


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
        categories = site.categories
        self.data = categories

    def post(self, request):
        data = request.data
        name = data['category']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
        new_category = site.create_category(name, category)
        site.categories.append(new_category)
        self.data = site.categories
        print(self.data)
