from datetime import date

from sqlalchemy.orm import Session

from models.services import Car, Company, Service, ServiceItem
from schemas.services import (
    CompanyCreate,
    ServiceCreate,
    ServiceItemCreate,
    ServiceItemUpdate,
    ServiceUpdate,
)


def get_companies(db: Session, name: str = None) -> list[Company]:
    query = db.query(Company)

    if name is not None:
        query = query.filter(Company.name.contains(name))

    return query.all()


def create_company(db: Session, data: CompanyCreate) -> Company:
    company = Company(name=data.name)
    db.add(company)
    db.commit()
    db.refresh()
    return company


def get_company_by_id(db: Session, company_id: int) -> Company:
    return db.query(Company).get(company_id)


def get_company_by_name(db: Session, name: str) -> Company:
    return db.query(Company).filter(Company.name == name).first()


def get_cars(db: Session, name: str = None) -> list[Car]:
    query = db.query(Car)

    if name is not None:
        query = query.filter(Car.name.icontains(name))

    return query.all()


def get_car_by_id(db: Session, car_id: int) -> Car:
    return db.query(Car).get(car_id)


def update_service_price(db: Session, service: Service) -> Service:
    s = 0
    items = service.items

    for item in items:
        s += item.price

    service.total_price = s
    db.commit()


def create_service(db: Session, user_id: int, data: ServiceCreate) -> Service:
    service = Service(
        mechanic=user_id,
        customer=data.customer,
        date=data.date,
        car=data.car,
        total_price=0,
    )

    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def get_user_services(
    db: Session,
    user_id: int,
    customer: str = None,
    start_date: date = None,
    end_date: date = None,
) -> list[Service]:
    query = db.query(Service).filter(Service.mechanic == user_id)

    if customer is not None:
        query = query.filter(Service.customer.icontains(customer))

    if start_date is not None:
        query = query.filter(Service.date >= start_date)

    if end_date is not None:
        query = query.filter(Service.date <= end_date)

    return query.all()


def get_service(db: Session, service_id: int) -> Service:
    return db.query(Service).get(service_id)


def validate_service(db: Session, service_id: int, user_id: int) -> bool:
    service = get_service(db, service_id)
    if service:
        return service.mechanic == user_id

    return False


def create_service_item(db: Session, data: ServiceItemCreate) -> ServiceItem:
    service_item = ServiceItem(service=data.service, price=data.price, title=data.title)
    db.add(service_item)
    db.commit()
    db.refresh(service_item)
    service = get_service(db, data.service)
    update_service_price(db, service)
    return service_item


def delete_service(db: Session, service: Service) -> Service:
    db.delete(service)
    db.commit()
    return service


def update_service(db: Session, service: Service, data: ServiceUpdate) -> Service:
    service.car = data.car
    service.customer = data.customer
    service.date = data.date
    db.commit()
    return service


def get_service_item(db: Session, item_id: id) -> ServiceItem:
    return db.query(ServiceItem).get(item_id)


def update_service_item(
    db: Session, service_item: ServiceItem, data: ServiceItemUpdate
) -> ServiceItem:
    service_item.title = data.title
    service_item.price = data.price
    db.commit()
    service = get_service(db, service_item.service)
    update_service_price(db, service)
    return service_item


def delete_service_item(db: Session, service_item: ServiceItem) -> ServiceItem:
    db.delete(service_item)
    db.commit()
    service = get_service(db, service_item.service)
    update_service_price(db, service)
    return service_item
