from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os
import csv

Base = declarative_base()

class Subject(Base):
    __tablename__ = 'subjects'

    code = Column(String, primary_key=True)
    subject_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    requirement = Column(String, nullable=False)
    credit = Column(Integer, nullable=False)
    semester_offered = Column(Integer, nullable=False)
    year_offered = Column(Integer, nullable=False)

    registrations = relationship("Registration", back_populates="subject")


class Registration(Base):
    __tablename__ = 'registrations'

    user_id = Column(Integer, primary_key=True)
    code = Column(String, ForeignKey('subjects.code'), primary_key=True)
    grade = Column(String, nullable=True)

    subject = relationship("Subject", back_populates="registrations")

class AvailableCourse(Base):
    __tablename__ = 'available_courses'
    user_id = Column(Integer, primary_key=True)
    code = Column(String, primary_key=True)
    subject_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    requirement = Column(String, nullable=False)
    credit = Column(Integer, nullable=False)
    semester_offered = Column(Integer, nullable=False)
    year_offered = Column(Integer, nullable=False)

engine = create_engine('sqlite:///database.db')  # SQLiteファイル
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, 'subjects.csv')
with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        subject = Subject(
            code=row['code'],
            subject_name=row['subject_name'],
            category=row['category'],
            requirement=row['requirement'],
            credit=int(row['credit']),
            semester_offered=int(row['semester_offered']),
            year_offered=int(row['year_offered'])
        )
        session.merge(subject)
    session.commit()

def get_session():
    return Session()
