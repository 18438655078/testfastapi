from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    password_hash = fields.CharField(max_length=128, null=True)
    mobile = fields.CharField(max_length=20, null=True)
    token = fields.CharField(max_length=50, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    # class PydanticMeta:
    #     exclude = ["password_hash"]


class UserInfo(models.Model):
    id = fields.IntField(pk=True)
    nickname = fields.CharField(max_length=20, unique=True)
    signature = fields.CharField(max_length=128, null=True)
    avatar = fields.CharField(max_length=20, null=True)
    user = fields.ForeignKeyField('models.Users', related_name='user_info')
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class UserThirdAuth(models.Model):
    id = fields.IntField(pk=True)
    uniq_id = fields.CharField(max_length=128, unique=True)
    login_type = fields.CharField(max_length=20, null=True)
    access_token = fields.CharField(max_length=128, null=True)
    user = fields.ForeignKeyField('models.Users', related_name='user_third_auth')
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class WechatAppUsers(models.Model):
    id = fields.IntField(pk=True)
    open_id = fields.CharField(max_length=128, unique=True)
    user = fields.ForeignKeyField('models.Users', related_name='wechat_app_user')
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)

UserInfo_Pydantic = pydantic_model_creator(UserInfo, name="UserInfo")
UserUserInfoIn_Pydantic = pydantic_model_creator(UserInfo, name="UserUserInfoIn", exclude_readonly=True)

UserThirdAuth_Pydantic = pydantic_model_creator(UserThirdAuth, name="UserThirdAuth")
UserThirdAuthIn_Pydantic = pydantic_model_creator(UserThirdAuth, name="UserThirdAuthIn", exclude_readonly=True)

WechatAppUsers_Pydantic = pydantic_model_creator(WechatAppUsers, name="WechatAppUsers")
WechatAppUsersIn_Pydantic = pydantic_model_creator(WechatAppUsers, name="WechatAppUsersIn", exclude_readonly=True)
