from fastapi import APIRouter, Depends, HTTPException

from models.users import User
from routers.users import get_current_user

router = APIRouter()


def is_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(400, detail="you are not admin")

    return user


@router.get("/")
async def me(user: User = Depends(is_admin)):
    print(user.username)
    return user.username
