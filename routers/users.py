from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from crud.users import authenticate_user, create_user, get_user
from database import get_db
from schemas.users import Token, UserBase, UserCreate
from utils import ALGORITHM, SECRET_KEY, create_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Any = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/signup")
async def signup(user: UserCreate, db=Depends(get_db)):
    if get_user(db, user.username):
        raise HTTPException(
            status_code=400, detail="user with this username already exists"
        )
    create_user(db, user)
    return UserBase(username=user.username)


@router.post("/login")
async def login(user: UserCreate, db=Depends(get_db)):
    user = authenticate_user(db, user.username, user.password)

    if not user:
        raise HTTPException(status_code=403, detail="username or password not correct")
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token)
