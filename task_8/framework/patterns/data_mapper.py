import threading
import sqlite3

CONNECTION = sqlite3.connect('project.sqlite')


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.obj_name = None
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, mapper_registry):
        self.mapper_registry = mapper_registry

    def register_new(self, obj, obj_name):
        self.obj_name = obj_name
        self.new_objects.clear()
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.clear()
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.clear()
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    def insert_new(self):
        print(self.new_objects)
        for obj in self.new_objects:
            self.mapper_registry.get_current_mapper(name=self.obj_name).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            self.mapper_registry.get_current_mapper(name=self.obj_name).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            self.mapper_registry.get_current_mapper(name=self.obj_name).delete(obj)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:

    def mark_new(self, obj_name):
        UnitOfWork.get_current().register_new(self, obj_name)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


class StudentMapper:

    def __init__(self, connection, mapper_object=None):
        self.connection = connection
        self.mapper_object = mapper_object
        self.cursor = connection.cursor()
        self.tablename = 'students'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            student_id, name, email = item
            student = self.mapper_object(name, email)
            student.id = student_id
            result.append(student)
        return result

    def find_by_id(self, student_id):
        statement = f"SELECT id, name, email FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (student_id,))
        result = self.cursor.fetchone()
        if result:
            return self.mapper_object(*result)
        else:
            raise RecordNotFoundException(f'record with id={student_id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, email) VALUES (?, ?)"
        self.cursor.execute(statement, (obj.name, obj.email))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=?, email=? WHERE id=?"
        self.cursor.execute(statement, (obj.name, obj.email, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class MapperRegistry:
    mappers = {
        'students': StudentMapper,
    }

    # @staticmethod
    # def get_mapper(obj):
    #     if isinstance(obj, Student):
    #         return StudentMapper(CONNECTION)

    @staticmethod
    def get_current_mapper(name, mapper_object=None):
        return MapperRegistry.mappers[name](CONNECTION, mapper_object)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Database commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Database update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Database delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
