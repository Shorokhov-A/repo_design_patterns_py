import json

from framework.view import View, TemplateView
from framework.patterns.generative_patterns import Engine, Logger
from framework.patterns.structural_patterns import AddRoute
from framework.patterns.structural_patterns import debug, DebugMethod

site = Engine()
logger = Logger('main')


@debug
@AddRoute(url='/')
class Homepage(TemplateView):

    template_name = 'index.html'

    def get(self, request):
        return 'GET SUCCESS'

    def post(self, request):
        return 'POST SUCCESS'


@AddRoute(url='/about/')
class AboutPage(TemplateView):

    template_name = 'about.html'


@AddRoute(url='/contacts/')
class Contacts(View):

    template_name = 'contacts.html'

    def get(self, request):
        return 'GET SUCCESS'

    def post(self, request):
        with open('message.json', 'w', encoding='utf-8') as f:
            json.dump(request.data, f)
        return 'POST SUCCESS'


@debug
@AddRoute(url='/create_category/')
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
        return 'POST SUCCESS'


@AddRoute(url='/create_course/')
class CreateCourse(View):
    template_name = 'create_course.html'
    category_id = -1

    def get(self, request):
        try:
            self.category_id = int(request.query_params['id'])
            category = site.find_category_by_id(int(self.category_id))
            self.data = {
                'objects_list': category.courses,
                'name': category.name,
                'id': category.id,
            }
        except KeyError:
            return 'No categories have been added yet'

    def post(self, request):
        data = request.data
        name = data['name']
        category = None
        if self.category_id != -1:
            category = site.find_category_by_id(int(self.category_id))
            course = site.create_course('video_course', name, category)
            site.courses.append(course)
        self.data = {
            'objects_list': category.courses,
            'name': category.name,
            'id': category.id,
        }


@AddRoute(url='/courses/')
class CoursesList(View):
    template_name = 'courses.html'

    def get(self, request):
        logger.log('Список курсов')
        self.data = site.categories


@AddRoute(url='/copy-course/')
class CourseCopy(View):
    template_name = 'create_course.html'

    def get(self, request):
        request_params = request.query_params
        print(f'Курсы {site.courses}')
        try:
            name = request_params['name']
            old_course = site.get_course(name)
            print(f'Старый курс {old_course}')
            if old_course:
                category = site.find_category_by_id(old_course.category.id)
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)
                category.courses.append(new_course)

            self.data = {
                'objects_list': category.courses,
                'name': category.name,
                'id': category.id,
            }
        except KeyError:
            return 'No courses have been added yet'


@AddRoute(url='/students/')
class StudentsList(View):
    template_name = 'students.html'

    def get(self, request):
        self.data = site.students


@AddRoute(url='/create-students/')
class CreateStudent(View):
    template_name = 'create_student.html'

    def post(self, request):
        data = request.data
        name = data['login']
        email = data['email']
        new_obj = site.create_user('student', name, email)
        site.students.append(new_obj)
