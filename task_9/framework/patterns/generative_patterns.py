import copy
from urllib.parse import unquote
from framework.patterns.behavioral_patterns import ConsoleWriter, Subject
from framework.patterns.data_mapper import DomainObject, MapperRegistry


class User:
    def __init__(self, name):
        self.name = name


class Teacher(User):
    pass


class Student(User, DomainObject):
    def __init__(self, name, email):
        self.courses = []
        self.email = email
        super().__init__(name)


# Абстрактная фабрика - фабрика пользователей.
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher,
    }

    # Фабричный метод
    @classmethod
    def create(cls, user_type, name, email):
        return cls.types[user_type](name, email)


# Категория
class Category(DomainObject):
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


# Прототип курса
class CoursePrototype:
    def clone(self):
        return copy.deepcopy(self)


# Курс
class Course(CoursePrototype, Subject, DomainObject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


# Интерактивный курс
class InteractiveCourse(Course):
    pass


# видеокурс
class VideoCourse(Course):
    pass


# Абстрактная фабрика - фабрика курсов
class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'video_course': VideoCourse,
    }

    # Фабричный метод
    @classmethod
    def create(cls, course_type, name, category):
        return cls.types[course_type](name, category)


# Основной класс проекта
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(user_type, name, email):
        return UserFactory.create(user_type, name, email)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, category_id):
        for item in self.categories:
            print(item, item.id)
            if item.id == category_id:
                return item
        raise Exception(f'Отсутствует катекория с id - {category_id}')

    def find_category_by_id_mapper(self, id):
        mapper = MapperRegistry.get_current_mapper('category', Category)
        return mapper.find_cat_by_id(id)

    @staticmethod
    def create_course(course_type, name, category):
        return CourseFactory.create(course_type, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(value):
        value_str = value.decode(encoding='utf-8').replace('+', ' ')
        value_str = unquote(value_str)
        return value_str


class SingletonByName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        self.writer.write(f'log--->{text}')
