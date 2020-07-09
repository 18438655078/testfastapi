from fastapi import APIRouter

from typing import List

from fastapi import HTTPException
from pydantic import BaseModel
from app.models import UserThirdAuth, WechatAppUsers
from app.models.users import UserThirdAuth_Pydantic, UserThirdAuthIn_Pydantic, WechatAppUsers_Pydantic, \
    WechatAppUsersIn_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError

router = APIRouter()


class Status(BaseModel):
    message: str


@router.post("/third_auth", response_model=UserThirdAuth_Pydantic)
async def create_third_auth(user: UserThirdAuthIn_Pydantic):
    user_obj = await UserThirdAuth.create(**user.dict(exclude_unset=True))
    return await UserThirdAuth_Pydantic.from_tortoise_orm(user_obj)


@router.get(
    "/third_auth/{pk}", response_model=UserThirdAuth_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_third_auth(pk: int):
    return await UserThirdAuth_Pydantic.from_queryset_single(UserThirdAuth.get(id=pk))


@router.post(
    "/third_auth/{pk}", response_model=UserThirdAuth_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_third_auth(pk: int, user: UserThirdAuthIn_Pydantic):
    await UserThirdAuth.filter(id=pk).update(**user.dict(exclude_unset=True))
    return await UserThirdAuth_Pydantic.from_queryset_single(UserThirdAuth.get(id=pk))


@router.delete("/third_auth/{pk}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_third_auth(pk: int):
    deleted_count = await UserThirdAuth.filter(id=pk).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {pk} not found")
    return Status(message=f"Deleted user {pk}")


# WechatApp
@router.post("/wechat_auth", response_model=WechatAppUsers_Pydantic)
async def create_wechat_auth(user: WechatAppUsersIn_Pydantic):
    user_obj = await WechatAppUsers.create(**user.dict(exclude_unset=True))
    return await WechatAppUsers_Pydantic.from_tortoise_orm(user_obj)


@router.get(
    "/wechat_auth/{pk}", response_model=WechatAppUsers_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_third_auth(pk: int):
    return await WechatAppUsers_Pydantic.from_queryset_single(WechatAppUsers.get(id=pk))


@router.post(
    "/wechat_auth/{pk}", response_model=WechatAppUsers_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_wechat_auth(pk: int, user: WechatAppUsersIn_Pydantic):
    await WechatAppUsers.filter(id=pk).update(**user.dict(exclude_unset=True))
    return await WechatAppUsers_Pydantic.from_queryset_single(WechatAppUsers.get(id=pk))


@router.delete("/wechat_auth/{pk}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_wechat_auth(pk: int):
    deleted_count = await WechatAppUsers.filter(id=pk).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {pk} not found")
    return Status(message=f"Deleted user {pk}")
