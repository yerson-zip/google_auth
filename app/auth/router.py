from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from app.auth.oauth import oauth
from app.auth.schemas import RegisterUser
from app.auth.service import google_info, login_service
from app.core.db import get_db, engine
from app.user.model import Base as base1
from app.auth.model import Base as base2

base1.metadata.create_all(bind=engine)
base2.metadata.create_all(bind=engine)

router = APIRouter()


@router.get("/auth/google")
async def auth_google(request: Request):
    return await oauth.google.authorize_redirect("http://localhost:8000/auth/google/callback")


@router.get("/auth/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    user_register = google_info(request)
    user = RegisterUser(email=user_register.get("email"),
                        full_name=user_register.get("name"),
                        picture=user_register.get("picture"))
    login_service(db=db, user_request=user)
