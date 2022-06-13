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
    context_objects_list = 'objects_list'
    context = {context_objects_list: None}
    request = None

    def get_context_data(self, *args, **kwargs):
        return self.context

    def get(self, request: Request, *args, **kwargs):
        self.request = request
        self.context.update(self.get_context_data(self))

    def get_template(self):
        return render(self.template_name, data_list=self.context)


class CreateView(ListView):

    def create_obj(self, *args, **kwargs):
        pass

    def post(self, request: Request, *args, **kwargs):
        self.request = request
        self.create_obj(self)
