
TORTOISE_ORM = {
    "connections": {"default": "mysql://damai:damai@localhost:3306/damai"},
    # "connections": {"default": "postgres://postgres:postgres@localhost:5432/damai"},
    "apps": {
        "models": {
            "models": ["app.models.users", "aerich.models"],
            # "models": ["aerich.models", "app.models.users"],
            # 须添加“aerich.models” 后者“models”是上述models.py文件的路径
            "default_connection": "default",
        },
    },
}

