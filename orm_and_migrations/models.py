from sqlalchemy import create_engine, Column, String, ForeignKey, SmallInteger, Integer, Date
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import date

engine = create_engine("postgresql+psycopg2://postgres:qwerty@localhost:5432/university", echo=True)
session = sessionmaker(bind=engine)()

Base = declarative_base()

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    students = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(120), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", back_populates="students")
    marks = relationship("Mark", back_populates="student")


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(120), nullable=False)
    subjects = relationship("Subject", back_populates="teacher")


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="subjects")
    marks = relationship("Mark", back_populates="subject")


class Mark(Base):
    __tablename__ = "marks"
    id = Column(Integer, primary_key=True)
    mark = Column(SmallInteger, nullable=False)
    mark_date = Column(Date, nullable=False, default=date.today)
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", back_populates="marks")
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    subject = relationship("Subject", back_populates="marks")


db_models = {
            "group": Group,
            "student": Student,
            "teacher": Teacher,
            "subject": Subject,
            "mark": Mark,
            }

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    session.commit()