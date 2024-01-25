from crud.users import create_user
from database import SessionLocal
from schemas.users import UserCreate

print("\nyou are creating admin user\n")
user = UserCreate(
    username=input("enter username : "), password=input("enter password : ")
)

create_user(SessionLocal(), user, True)
