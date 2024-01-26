from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.services import (
    create_service,
    create_service_item,
    delete_service,
    delete_service_item,
    get_car_by_id,
    get_cars,
    get_companies,
    get_company_by_id,
    get_service,
    get_service_item,
    get_user_services,
    update_service,
    update_service_item,
    validate_service,
)
from database import get_db
from models.users import User
from routers.users import get_current_user
from schemas.services import (
    CarDetail,
    CompanyDetail,
    CompanyItem,
    ServiceCreate,
    ServiceInDB,
    ServiceItemCreate,
    ServiceItemInDB,
    ServiceItemUpdate,
    ServiceUpdate,
)

router = APIRouter()


@router.get("/", response_model=list[ServiceInDB])
async def service_list(
    customer: str = None,
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    services = get_user_services(db, user.id, customer, start_date, end_date)
    return services


@router.post("/", response_model=ServiceInDB)
async def service_create(
    data: ServiceCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not get_car_by_id(db, data.car):
        raise HTTPException(status_code=404)

    return create_service(db, user.id, data)


@router.post("/item", response_model=ServiceItemInDB)
async def service_item_create(
    data: ServiceItemCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not validate_service(db, data.service, user.id):
        raise HTTPException(status_code=404)

    return create_service_item(db, data)


@router.get("/company", response_model=list[CompanyItem])
async def company_list(
    name: str = None, _: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_companies(db, name)


@router.get("/car", response_model=list[CarDetail])
async def car_list(
    name: str = None, _: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_cars(db, name)


@router.put("/item/{item_id}", response_model=ServiceItemInDB)
async def service_item_update(
    item_id: int,
    data: ServiceItemUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service_item = get_service_item(db, item_id)

    if validate_service(db, service_item.id, user.id):
        raise HTTPException(404)

    return update_service_item(db, service_item, data)


@router.delete("/item/{item_id}")
async def service_item_delete(
    item_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    service_item = get_service_item(db, item_id)

    if validate_service(db, service_item.id, user.id):
        raise HTTPException(404)

    return delete_service_item(db, service_item)


@router.get("/car/{car_id}", response_model=CarDetail)
async def car_detail(
    car_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    car = get_car_by_id(db, car_id)

    if not car:
        raise HTTPException(status_code=404, detail="car with this id not found")

    return car


@router.get("/company/{company_id}", response_model=CompanyDetail)
async def company_detail(
    company_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    company = get_company_by_id(db, company_id)

    if not company:
        raise HTTPException(status_code=404, detail="company with this id not found")

    return company


@router.get("/{service_id}", response_model=ServiceInDB)
async def service_detail(
    service_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not validate_service(db, service_id, user.id):
        raise HTTPException(status_code=404)

    return get_service(db, service_id)


@router.delete("/{service_id}", response_model=ServiceInDB)
async def service_delete(
    service_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not validate_service(db, service_id, user.id):
        raise HTTPException(status_code=404)

    service = get_service(db, service_id)
    return delete_service(db, service)


@router.put("/{service_id}", response_model=ServiceInDB)
async def service_update(
    service_id: int,
    data: ServiceUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not validate_service(db, service_id, user.id):
        raise HTTPException(status_code=404)

    if not get_car_by_id(db, data.car):
        raise HTTPException(status_code=404)

    service = get_service(db, service_id)
    return update_service(db, service, data)
