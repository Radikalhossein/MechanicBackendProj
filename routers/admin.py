from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.admin import (
    check_unique_car,
    create_car,
    create_company,
    delete_car,
    delete_company,
    delete_user,
    get_services,
    get_user_by_id,
    get_users,
    update_car,
    update_company,
    update_user,
)
from crud.services import (
    delete_service,
    delete_service_item,
    get_car_by_id,
    get_cars,
    get_companies,
    get_company_by_id,
    get_company_by_name,
    get_service,
    get_service_item,
    update_service,
    update_service_item,
)
from crud.users import create_user, get_user
from database import get_db
from models.users import User
from routers.users import get_current_user
from schemas.admin import (
    CarUpdate,
    CompanyUpdate,
    ServiceInDB,
    UserCreate,
    UserItem,
    UserList,
    UserUpdate,
)
from schemas.services import (
    CarCreate,
    CarDetail,
    CarItem,
    CompanyCreate,
    CompanyDetail,
    CompanyItem,
    ServiceItemInDB,
    ServiceItemUpdate,
    ServiceUpdate,
)

router = APIRouter()


def is_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(400, detail="you are not admin")

    return user


@router.get("/user", response_model=UserList)
async def user_list(
    username: str = None,
    is_admin: bool = None,
    _: User = Depends(is_admin),
    db=Depends(get_db),
):
    return get_users(db, is_admin, username)


@router.get("/user/{user_id}", response_model=UserItem)
async def user_detail(user_id: int, _: User = Depends(is_admin), db=Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if user:
        return user

    raise HTTPException(404, detail="user with this id not found")


@router.delete("/user/{user_id}", response_model=UserItem)
async def user_delete(user_id: int, _: User = Depends(is_admin), db=Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if user:
        delete_user(db, user)
        return user

    raise HTTPException(404, detail="user with this id not found")


@router.post("/user", response_model=UserItem)
async def user_create(
    user: UserCreate, _: User = Depends(is_admin), db=Depends(get_db)
):
    if get_user(db, user.username):
        raise HTTPException(
            status_code=400, detail="user with this username already exists"
        )

    db_user = create_user(db, user, is_admin=user.is_admin)
    return db_user


@router.put("/user/{user_id}", response_model=UserItem)
async def user_update(
    user_id: int,
    new_data: UserUpdate,
    _: User = Depends(is_admin),
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, user_id)

    if user.username != new_data.username and get_user(db, new_data.username):
        raise HTTPException(
            status_code=400, detail="user with this username already exists"
        )

    if not user:
        raise HTTPException(status_code=404, detail="user with this id not found")

    update_user(db, user, new_data)
    return user


@router.get("/company", response_model=list[CompanyItem])
async def company_list(
    name: str = None, _: User = Depends(is_admin), db: Session = Depends(get_db)
):
    return get_companies(db, name)


@router.post("/company", response_model=CompanyItem)
async def company_create(
    data: CompanyCreate, _: User = Depends(is_admin), db: Session = Depends(get_db)
):
    if get_company_by_name(db, data.name):
        raise HTTPException(status_code=400, detail="company with this name exists")

    company = create_company(db, data)
    return company


@router.get("/company/{company_id}", response_model=CompanyDetail)
async def company_detail(
    company_id: int, _: User = Depends(is_admin), db: Session = Depends(get_db)
):
    company = get_company_by_id(db, company_id)

    if not company:
        raise HTTPException(status_code=404, detail="company with this id not found")

    return company


@router.delete("/company/{company_id}", response_model=CompanyItem)
async def company_delete(
    company_id: int, _: User = Depends(is_admin), db: Session = Depends(get_db)
):
    company = get_company_by_id(db, company_id)

    if not company:
        raise HTTPException(status_code=404, detail="company with this id not found")

    return delete_company(db, company)


@router.put("/company/{company_id}", response_model=CompanyItem)
async def company_update(
    company_id: int,
    data: CompanyUpdate,
    _: User = Depends(is_admin),
    db: Session = Depends(get_db),
):
    company = get_company_by_id(db, company_id)

    if not company:
        raise HTTPException(status_code=404, detail="company with this id not found")

    if get_company_by_name(db, data.name):
        raise HTTPException(status_code=403, detail="company with this name exists")

    return update_company(db, company, data)


@router.post("/car", response_model=CarItem)
async def car_create(
    data: CarCreate, _: User = Depends(is_admin), db: Session = Depends(get_db)
):
    company = get_company_by_id(db, data.company)
    if not company:
        raise HTTPException(status_code=400, detail="company with this id not found")

    if check_unique_car(db, company, data.name):
        raise HTTPException(status_code=400, detail="company has car with same name")

    car = create_car(db, data)
    return car


@router.get("/car", response_model=list[CarDetail])
async def car_list(
    name: str = None, _: User = Depends(is_admin), db: Session = Depends(get_db)
):
    return get_cars(db, name)


@router.get("/car/{car_id}", response_model=CarDetail)
async def car_detail(
    car_id: int, _: User = Depends(is_admin), db: Session = Depends(get_db)
):
    car = get_car_by_id(db, car_id)

    if not car:
        raise HTTPException(status_code=404, detail="car with this id not found")

    return car


@router.delete("/car/{car_id}", response_model=CarDetail)
async def car_delete(
    car_id: int, _: User = Depends(is_admin), db: Session = Depends(get_db)
):
    car = get_car_by_id(db, car_id)

    if not car:
        raise HTTPException(status_code=404, detail="car with this id not found")

    return delete_car(db, car)


@router.put("/car/{car_id}", response_model=CarDetail)
async def car_update(
    car_id: int,
    data: CarUpdate,
    _: User = Depends(is_admin),
    db: Session = Depends(get_db),
):
    car = get_car_by_id(db, car_id)

    if not car:
        raise HTTPException(status_code=404, detail="car not found")

    company = get_company_by_id(db, data.company)
    if not company:
        raise HTTPException(status_code=400, detail="company with this id not found")

    if check_unique_car(db, company, data.name):
        raise HTTPException(status_code=400, detail="company has car with same name")

    car = update_car(db, car, data)
    return car


@router.get("/service", response_model=list[ServiceInDB])
async def service_list(
    customer: str = None,
    mechanic: int = None,
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db),
    _: User = Depends(is_admin),
):
    return get_services(db, customer, mechanic, start_date, end_date)


@router.get("/service/{service_id}", response_model=ServiceInDB)
async def service_detail(
    service_id: int, db: Session = Depends(get_db), _: User = Depends(is_admin)
):
    return get_service(db, service_id)


@router.put("/service/{service_id}", response_model=ServiceInDB)
async def service_update(
    service_id: int,
    data: ServiceUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(is_admin),
):
    service = get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404)
    return update_service(db, service, data)


@router.delete("/service/{service_id}", response_model=ServiceInDB)
async def service_delete(
    service_id: int, db: Session = Depends(get_db), _: User = Depends(is_admin)
):
    service = get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404)

    return delete_service(db, service)


@router.put("/item/{item_id}", response_model=ServiceItemInDB)
async def service_item_update(
    item_id: int,
    data: ServiceItemUpdate,
    _: User = Depends(is_admin),
    db: Session = Depends(get_db),
):
    item = get_service_item(db, item_id)

    if not item:
        raise HTTPException(status_code=404)

    return update_service_item(db, item, data)


@router.delete("/item/{item_id}", response_model=ServiceItemInDB)
async def service_item_delete(
    item_id: int, db: Session = Depends(get_db), _: User = Depends(is_admin)
):
    item = get_service_item(db, item_id)

    if not item:
        raise HTTPException(status_code=404)

    return delete_service_item(db, item)
