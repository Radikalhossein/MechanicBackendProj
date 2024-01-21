from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str


class CarCreate(BaseModel):
    name: str
    company_id: int
