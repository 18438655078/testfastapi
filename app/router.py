from fastapi import APIRouter

from app.views import users, user_info, account

bprouter = APIRouter()

bprouter.include_router(users.router, tags=['users'])
bprouter.include_router(user_info.router, tags=['user_info'])
bprouter.include_router(account.router, tags=['account'], prefix='/account')
