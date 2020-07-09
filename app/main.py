from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from app.router import bprouter
from app.core.config import API_PREFIX
from app.core.error import http422_error_handler, http_error_handler
import uvicorn
from app.settings.settings import TORTOISE_ORM


def get_app() -> FastAPI:
    app = FastAPI(title="barley")

    app.add_middleware(
        CORSMiddleware,
        # allow_origins=ALLOWED_HOSTS or ["*"],
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_tortoise(app, TORTOISE_ORM, generate_schemas=True, add_exception_handlers=True)

    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)    
    app.include_router(bprouter, prefix=API_PREFIX)
    return app


if __name__ == '__main__':
    app = get_app()
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
