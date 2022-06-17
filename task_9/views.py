import json

from framework.view import View, TemplateView, ListView, CreateView
from framework.patterns.generative_patterns import Engine, Logger, Student, Category
from framework.patterns.structural_patterns import AddRoute, debug, DebugMethod
from framework.patterns.behavioral_patterns import EmailNotifier, SmsNotifier, BaseSerializer
from framework.patterns.data_mapper import UnitOfWork, MapperRegistry

site = Engine()
logger = Logger('main')

email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


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


@debug
@AddRoute(url='/create_category/')
class CreateCategory(CreateView):

    template_name = 'create_category.html'

    def get_context_data(self):
        context = super().get_context_data(self)
        mapper = MapperRegistry.get_current_mapper('category', Category)
        context.update({self.context_objects_list: mapper.all()})
        return context

    def create_obj(self, *args, **kwargs):
        data = self.request.data
        name = data['category']
        new_category = site.create_category(name)
        site.categories.append(new_category)
        new_category.mark_new('category')
        UnitOfWork.get_current().commit()


@AddRoute(url='/create_course/')
class CreateCourse(CreateView):
    template_name = 'create_course.html'
    category_id = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(self)
        try:
            self.category_id = int(self.request.query_params['id'])
            # category = site.find_category_by_id(int(self.category_id))
            category = site.find_category_by_id_mapper(int(self.category_id))
            print(category.name)
            context.update({
                'objects_list': category.courses,
                'name': category.name,
                # 'id': category.id
            })
            return context
        except KeyError:
            return 'No categories have been added yet'

    def create_obj(self, *args, **kwargs):
        data = self.request.data
        name = data['name']
        # category = site.find_category_by_id(int(self.category_id))
        category = site.find_category_by_id_mapper(int(self.category_id))
        course = site.create_course('video_course', name, category)
        course.observers.append(email_notifier)
        course.observers.append(sms_notifier)
        site.courses.append(course)
        course.mark_new('course')
        UnitOfWork.get_current().commit()


@AddRoute(url='/courses/')
class CoursesList(ListView):
    template_name = 'courses.html'

    def get_context_data(self):
        context = super().get_context_data(self)
        mapper = MapperRegistry.get_current_mapper('category', Category)
        context.update({self.context_objects_list: mapper.all()})
        return context


@AddRoute(url='/copy-course/')
class CourseCopy(ListView):
    template_name = 'create_course.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(self)
        request_params = self.request.query_params
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
            context.update({
                'objects_list': category.courses,
                'name': category.name,
                'id': category.id,
            })
            return context
        except KeyError:
            return 'No courses have been added yet'


@AddRoute(url='/students/')
class StudentsList(ListView):
    template_name = 'students.html'

    def get_context_data(self):
        context = super().get_context_data(self)
        mapper = MapperRegistry.get_current_mapper('students', Student)
        context.update({self.context_objects_list: mapper.all()})
        return context


@AddRoute(url='/create-students/')
class CreateStudent(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, *args, **kwargs):
        data = self.request.data
        name = data['login']
        email = data['email']
        new_obj = site.create_user('student', name, email)
        site.students.append(new_obj)
        new_obj.mark_new('students')
        UnitOfWork.get_current().commit()


@AddRoute(url='/add-student/')
class AddStudentToCourse(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self, *args, **kwargs):
        students = MapperRegistry.get_current_mapper('students', Student).all()
        context = {
            'courses': site.courses,
            'students': students,
        }
        return context

    def create_obj(self, *args, **kwargs):
        data = self.request.data
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
