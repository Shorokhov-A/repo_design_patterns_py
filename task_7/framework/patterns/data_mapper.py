import sqlite3

from framework.patterns.generative_patterns import Student

CONNECTION = sqlite3.connect('project.sqlite')


class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'students'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            student_id, name, email = item
            student = Student(name, email)
            student.id = student_id
            result.append(student)
        return result

    def find_by_id(self, student_id):
        statement = f"SELECT id, name, email FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (student_id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
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

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(CONNECTION)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](CONNECTION)


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