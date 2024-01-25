from typing import List

from pydantic import BaseModel


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
