from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Subject(Base):
    __tablename__ = 'subjects'

    code = Column(String, primary_key=True)
    subject_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    requirement = Column(String, nullable=False)
    credit = Column(Integer, nullable=False)
    term = Column(String, nullable=False)

    registrations = relationship("Registration", back_populates="subject")


class Registration(Base):
    __tablename__ = 'registrations'

    user_id = Column(Integer, primary_key=True)
    code = Column(String, ForeignKey('subjects.code'), primary_key=True)

    subject = relationship("Subject", back_populates="registrations")