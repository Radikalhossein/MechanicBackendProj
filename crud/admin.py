from datetime import date

from sqlalchemy.orm import Session

from models.services import Car, Company, Service, ServiceItem
from models.users import User
from schemas.admin import CarUpdate, CompanyUpdate, UserUpdate
from schemas.services import CarCreate, CompanyCreate


def get_users(db: Session, is_admin: bool = None, username: str = None) -> list[User]:
    query = db.query(User)

    if is_admin is not None:
        query = query.filter(User.is_admin == is_admin)

    if username is not None:
        query = query.filter(User.username.contains(username))

    return query.all()


def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).get(user_id)


def delete_user(db: Session, user: User) -> User:
    db.delete(user)
    db.commit()
    return user


def update_user(db: Session, user: User, user_new: UserUpdate) -> User:
    user.username = user_new.username
    user.is_admin = user_new.is_admin
    db.commit()
    return user


def create_company(db: Session, data: CompanyCreate) -> Company:
    company = Company(name=data.name)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def delete_company(db: Session, company: Company) -> Company:
    db.query(Car).filter(Car.company == company.id).delete()
    db.delete(company)
    db.commit()
    return company


def create_car(db: Session, data: CarCreate) -> Car:
    car = Car(name=data.name, company=data.company)
    db.add(car)
    db.commit()
    db.refresh(car)
    return car


def delete_car(db: Session, car: Car) -> Car:
    db.delete(car)
    db.commit()
    return car


def update_car(db: Session, car: Car, data: CarUpdate):
    car.name = data.name
    car.company = data.company
    db.commit()
    return car


def update_company(db: Session, company: Company, data: CompanyUpdate):
    company.name = data.name
    db.commit()
    return company


def check_unique_car(db: Session, company: Company, name: str):
    return (
        db.query(Car).filter(Car.company == company.id).filter(Car.name == name).all()
    )


def get_services(
    db: Session,
    customer: str = None,
    mechanic: int = None,
    start_date: date = None,
    end_date: date = None,
) -> list[Service]:
    query = db.query(Service)

    if customer is not None:
        query = query.filter(Service.customer.icontains(customer))

    if mechanic is not None:
        query = query.filter(Service.mechanic == mechanic)

    if start_date is not None:
        query = query.filter(Service.date > start_date)

    if end_date is not None:
        query = query.filter(Service.date < end_date)

    return query
