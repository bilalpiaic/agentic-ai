from tabnanny import check
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


from sqlalchemy import Column, Integer, String, Boolean,CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# class Address(Base):
#     __tablename__ = "address"
    
#     id = Column(Integer, primary_key=True, index=True)
#     zip_code = Column(String, index=True)
#     street = Column(String, nullable=True)
#     city = Column(String, nullable=True)
#     user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    
class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, CheckConstraint('value > 5'),  index=True)
    email = Column(String, CheckConstraint('email ~* "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"'), nullable=False, unique=True, ) # type: ignore
    password = Column(String, nullable=True)




class Todos(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)