from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from app.auth.router import router

from app.core import config
app = FastAPI()

app.add_middleware( SessionMiddleware,
    secret_key=config.SECRET_KEY,
    same_site="lax",
    https_only=False,)

app.include_router(router)