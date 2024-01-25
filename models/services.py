from sqlalchemy import (
    DECIMAL,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
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

    services = relationship("Service")

    __table_args__ = (UniqueConstraint("name", "company", name="uq_name_comp"),)


class Service(Base):
    __tablename__ = "service"
    id = Column(Integer, primary_key=True)
    mechanic = Column(Integer, ForeignKey("user.id"))
    customer = Column(String)
    date = Column(Date)
    total_price = Column(DECIMAL)
    car = Column(Integer, ForeignKey("car.id"))

    items = relationship("ServiceItem")


class ServiceItem(Base):
    __tablename__ = "service_item"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(DECIMAL)
    service = Column(Integer, ForeignKey("service.id"))
