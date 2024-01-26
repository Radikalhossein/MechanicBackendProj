from typing import List

from pydantic import BaseModel

from schemas.services import ServiceInDBBase, ServiceItemBase


class UserBase(BaseModel):
    username: str
    is_admin: bool


class UserItem(UserBase):
    id: int


UserList = List[UserItem]


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class ServiceInDB(ServiceInDBBase):
    items: list[ServiceItemBase]
    mechanic: int


class CarUpdate(BaseModel):
    company: int
    name: str


class CompanyUpdate(BaseModel):
    name: str
