from fastapi import APIRouter

from typing import List

from fastapi import HTTPException
from pydantic import BaseModel

from app.models.users import User_Pydantic, UserIn_Pydantic, Users
from tortoise.contrib.fastapi import HTTPNotFoundError

router = APIRouter()


class Status(BaseModel):
    message: str


@router.get("/users", response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@router.post("/users", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.get(
    "/users/{pk}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(pk: int):
    return await User_Pydantic.from_queryset_single(Users.get(id=pk))


@router.post(
    "/users/{pk}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_user(pk: int, user: UserIn_Pydantic):
    await Users.filter(id=pk).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(Users.get(id=pk))


@router.delete("/users/{pk}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(pk: int):
    deleted_count = await Users.filter(id=pk).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {pk} not found")
    return Status(message=f"Deleted user {pk}")

