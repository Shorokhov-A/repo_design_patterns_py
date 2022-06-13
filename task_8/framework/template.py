from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    environment = Environment()
    environment.loader = FileSystemLoader(folder)
    template = environment.get_template(template_name)
    return template.render(**kwargs)


if __name__ == '__main__':
    output_test = render('index.html')
    print(output_test)
