from framework.view import View


class Homepage(View):

    template_name = 'index.html'

    def get(self, request):
        return 'GET SUCCESS'

    def post(self, request):
        return 'POST SUCCESS'


class AboutPage(View):
    template_name = 'about.html'
