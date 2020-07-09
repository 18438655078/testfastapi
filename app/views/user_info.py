from fastapi import APIRouter

from typing import List

from fastapi import HTTPException
from pydantic import BaseModel

from app.models.users import UserInfo_Pydantic, UserUserInfoIn_Pydantic, UserInfo
from tortoise.contrib.fastapi import HTTPNotFoundError

router = APIRouter()


class Status(BaseModel):
    message: str


@router.get("/user_info", response_model=List[UserInfo_Pydantic])
async def get_user_info_list():
    return await UserInfo_Pydantic.from_queryset(UserInfo.all())


@router.post("/user_info", response_model=UserInfo_Pydantic)
async def create_user_info(user: UserUserInfoIn_Pydantic):
    user_obj = await UserInfo.create(**user.dict(exclude_unset=True))
    return await UserInfo_Pydantic.from_tortoise_orm(user_obj)


@router.get(
    "/user_info/{pk}", response_model=UserInfo_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_user_info(pk: int):
    return await UserInfo_Pydantic.from_queryset_single(UserInfo.get(id=pk))


@router.post(
    "/user_info/{pk}", response_model=UserInfo_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_user_info(pk: int, user: UserUserInfoIn_Pydantic):
    await UserInfo.filter(id=pk).update(**user.dict(exclude_unset=True))
    return await UserInfo_Pydantic.from_queryset_single(UserInfo.get(id=pk))


@router.delete("/user_info/{pk}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user_info(pk: int):
    deleted_count = await UserInfo.filter(id=pk).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"UserInfo {pk} not found")
    return Status(message=f"Deleted user_info {pk}")

