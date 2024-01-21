from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    cars = relationship("Car")


class Car(Base):
    __tablename__ = "car"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    company = Column(Integer, ForeignKey("company.id"))


class Service:
    ...


class ServiceItem:
    ...
