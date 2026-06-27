from authlib.integrations.starlette_client import OAuth
from sentry_sdk import client

from app.core import config

oauth = OAuth()

oauth.register(
    name="google",
    client_id=config.GOOGLE_CLIENTE_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    server_metadata_url= "https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
