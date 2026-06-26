from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
import secrets

from app.utils import config
app = FastAPI()

app.add_middleware( SessionMiddleware,
    secret_key=config.SECRET_KEY,
    same_site="lax",
    https_only=False,)

oauth = OAuth()
oauth.register(
    name="google",
    client_id=config.GOOGLE_CLIENTE_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@app.get("/auth/google")
async def auth_google(request:Request):
    return await oauth.google.authorize_redirect(request,redirect_uri="https://google-auth-cbnp.onrender.com/auth/google/callback")

@app.get("/auth/google/callback")
async def google_callback(request:Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info= token.get("userinfo") or {}

        username = user_info.get("email")

        return {
            "email":username,
            "info":user_info
        }

    except Exception as e:
        return {"error":str(e)}