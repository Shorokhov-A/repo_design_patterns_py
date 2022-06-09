import json

from framework.view import View, TemplateView, ListView, CreateView
from framework.patterns.generative_patterns import Engine, Logger
from framework.patterns.structural_patterns import AddRoute, debug, DebugMethod
from framework.patterns.behavioral_patterns import EmailNotifier, SmsNotifier, BaseSerializer

site = Engine()
logger = Logger('main')

email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


@debug
@AddRoute(url='/')
class Homepage(TemplateView):

    template_name = 'index.html'


@AddRoute(url='/about/')
class AboutPage(TemplateView):

    template_name = 'about.html'


@AddRoute(url='/contacts/')
class Contacts(CreateView):

    template_name = 'contacts.html'

    def get(self, request):
        return 'GET SUCCESS'

    def post(self, request):
        with open('message.json', 'w', encoding='utf-8') as f:
            json.dump(request.data, f)
        return 'POST SUCCESS'


# @debug
# @AddRoute(url='/create_category/')
# class CreateCategory(View):
#
#     template_name = 'create_category.html'
#
#     def get(self, request):
#         categories = site.categories
#         self.data = categories
#
#     def post(self, request):
#         data = request.data
#         name = data['category']
#         category_id = data.get('category_id')
#         category = None
#         if category_id:
#             category = site.find_category_by_id(int(category_id))
#         new_category = site.create_category(name, category)
#         site.categories.append(new_category)
#         self.data = site.categories
#         print(self.data)
#         return 'POST SUCCESS'
@debug
@AddRoute(url='/create_category/')
class CreateCategory(CreateView):

    template_name = 'create_category.html'
    data = site.categories

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
class CreateCourse(CreateView):
    template_name = 'create_course.html'
    category_id = -1

    def get(self, request):
        try:
            self.category_id = int(request.query_params['id'])
            category = site.find_category_by_id(int(self.category_id))
            # self.data = {
            #     'objects_list': category.courses,
            #     'name': category.name,
            #     'id': category.id,
            # }
            self.context = {
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
            course.observers.append(email_notifier)
            course.observers.append(sms_notifier)
            site.courses.append(course)
        self.context = {
            'objects_list': category.courses,
            'name': category.name,
            'id': category.id,
        }


@AddRoute(url='/courses/')
class CoursesList(ListView):
    template_name = 'courses.html'
    data = site.categories


@AddRoute(url='/copy-course/')
class CourseCopy(ListView):
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

            # self.data = {
            #     'objects_list': category.courses,
            #     'name': category.name,
            #     'id': category.id,
            # }
            self.context = {
                'objects_list': category.courses,
                'name': category.name,
                'id': category.id,
            }
        except KeyError:
            return 'No courses have been added yet'


@AddRoute(url='/students/')
class StudentsList(ListView):
    template_name = 'students.html'
    data = site.students


@AddRoute(url='/create-students/')
class CreateStudent(CreateView):
    template_name = 'create_student.html'

    def post(self, request):
        data = request.data
        name = data['login']
        email = data['email']
        new_obj = site.create_user('student', name, email)
        site.students.append(new_obj)


@AddRoute(url='/add-student/')
class AddStudentToCourse(CreateView):
    template_name = 'add_student.html'
    context = {
        'courses': site.courses,
        'students': site.students,
    }

    def get(self, request):
        return self.context

    def post(self, request):
        data = request.data
        course_name = data['course_name']
        course = site.get_course(course_name)
        student_name = data['student_name']
        student = site.get_student(student_name)
        course.add_student(student)


@AddRoute(url='/api/')
class CourseApi(TemplateView):
    template_name = 'api.html'

    def get(self, request):
        return BaseSerializer(site.courses).save()
