from framework.request import Request
from framework.template import render


class View:

    def get(self, request: Request, *args, **kwargs):
        pass

    def post(self, request: Request, *args, **kwargs):
        pass


class TemplateView(View):
    template_name = None

    def get_template(self):
        return render(self.template_name)


class ListView(TemplateView):
    data = None
    context = None

    def get(self, request: Request, *args, **kwargs):
        self.context = {'objects_list': self.data}

    def get_template(self):
        return render(self.template_name, data_list=self.context)


class CreateView(ListView):
    def post(self, request: Request, *args, **kwargs):
        pass
