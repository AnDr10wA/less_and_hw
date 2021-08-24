'''
Создать таблицу Студент(Student) с помощью sqlalchemy. Студент
характеризуется именем(firstname) и фамилией (lastname) и группой к которой
он приурочен. Создать две группы. Добавить в каждую по три студента
'''
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, backref
from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, String, Float

DB_USER='postgres'
DB_PASSWORD='postgres'
DB_NAME='test'
DB_ECHO = True

Base = declarative_base()

class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "{}".format(self.name)

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    group_id = Column(Integer, ForeignKey('group.id'))
    group = relationship('Group', back_populates='students')


class Diary(Base):
    __tablename__ = "diary"
    id = Column(Integer, primary_key= True)
    average = Column(Float)
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship('Student', back_populates='diatyes')

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key= True)
    name = Column(String)
    pages = Column(Integer)
    students_id = Column(Integer, ForeignKey('student.id'))
    student = relationship('Student', back_populates = 'books')


class StudentBook(Base):
    __tablename__ = 'student_book'
    id = Column(Integer, primary_key= True)
    student_id = Column(Integer(), ForeignKey('student.id'))
    book_id = Column(Integer(), ForeignKey('book.id'))
    student = relationship('StudentBook', backref('book'))
    books = relationship('StudentBook', backref('student'))
    extra_data = Column(String(100))




Group.students = relationship('Student', order_by=Student.id, back_populates = 'group')
Student.diatyes = relationship("Diary", order_by = Diary.id, back_populates = 'student')
Student.StudentBook = relationship('student_book', order_by = StudentBook.id, back_populates = 'student' )
Book.StudentBook = relationship('student_book', order_by = StudentBook.id, back_populates = 'book')


engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}')
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
student = session.query(Student).get(1)

# group1 = Group(name='Luckies')
# student1 = Student(firstname='Ivan', lastname='Petrov', group=group1)
# student2 = Student(firstname='Petr', lastname='Ivanov', group=group1)
#
# group2 = Group(name='Loosers')
# student3 = Student(firstname='John', lastname='Doe', group=group2)
# student4 = Student(firstname='Jane', lastname='Doe', group=group2)
# student5 = Student(firstname='Test', lastname='Check', group=group2)
#
# diary1 = Diary(average = 8.9, student=student[0])
# diary2 = Diary(average = 9.9, student=student[1])
# diary3 = Diary(average = 6.1, student=student[2])
# diary4 = Diary(average = 5.3, student=student[3])
# diary5 = Diary(average = 4.5, student=student[4])
book1 = Book(name = "Harry Potter", pages = 500, StudentBook=student)
book2 = Book(name = "Python Developer", pages = 400)
book3 = Book(name = "Konek Gorbunok", pages = 100)
book4 = Book(name = "Hobbit", pages = 550)
book5 = Book(name = "The Lord of the Rings", pages = 800)

session.add_all([book1, book2, book3, book4, book5])
session.commit()
