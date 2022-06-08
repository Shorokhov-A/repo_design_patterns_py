from framework.request import Request
from framework.template import render


class View:

    # template_name = None
    # data = {}

    def get(self, request: Request, *args, **kwargs):
        pass

    def post(self, request: Request, *args, **kwargs):
        pass

    # @classmethod
    # def get_template(cls):
    #     return render(cls.template_name, data_list=cls.data)


class TemplateView(View):
    template_name = None

    def get_template(self):
        return render(self.template_name)


class ListView(TemplateView):
    data = {}

    @classmethod
    def get_template(cls):
        return render(cls.template_name, data_list=cls.data)
