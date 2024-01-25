import datetime

from pydantic import BaseModel, Field


class CompanyBase(BaseModel):
    name: str


class CompanyItem(CompanyBase):
    id: int


class CarBase(BaseModel):
    name: str


class CarItem(CarBase):
    id: int


class CompanyDetail(CompanyItem):
    cars: list[CarItem]


class CompanyCreate(CompanyBase):
    pass


class CarCreate(CarBase):
    company: int


class CarDetail(CarCreate, CarItem):
    pass


class ServiceBase(BaseModel):
    customer: str
    date: datetime.date
    car: int


class ServiceCreate(ServiceBase):
    date: datetime.date = Field(default_factory=datetime.date.today)


class ServiceUpdate(ServiceCreate):
    pass


class ServiceInDBBase(ServiceBase):
    id: int


class ServiceItemBase(BaseModel):
    title: str
    price: int


class ServiceItemCreate(ServiceItemBase):
    service: int


class ServiceItemUpdate(ServiceItemCreate):
    pass


class ServiceItemInDB(ServiceItemBase):
    id: int


class ServiceInDB(ServiceInDBBase):
    items: list[ServiceItemBase]
