import secrets

import bcrypt
from fastapi import HTTPException, Request
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta

from pydantic_settings.sources.providers import secrets
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.model import RefreshToken
from app.auth.schemas import RegisterUser
from app.core import config
from app.user.model import User
from app.user.service import get_user_by_email, create_user
from app.auth.oauth import oauth

def create_access_token(data: dict) -> str:
    payload = {
        "sub": str(data["id"]),
        "rol": data["rol"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=int(config.ACCESS_TOKEN_EXPIRE_MINUTES))
    }

    return jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)


def verification_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=config.ALGORITHM)
        return payload
    except JWTError:
        return None


def login_service(db:Session, user_request:RegisterUser ):
    user = get_user_by_email(db,user_request.email)

    if user is None:
        user = create_user(db, user_request)

    access_token = create_access_token(data={
        "id":user.id,
        "rol":user.rol
    })

    refresh_token = create_refresh_token(user_id=user.id, db=db)
    return {
        "access_token":access_token,
        "refresh_token": refresh_token
    }


def create_refresh_token(user_id: int, db: Session) -> str:
    token = secrets.token_hex(32)
    hashed  = bcrypt.hashpw(token.encode(), bcrypt.gensalt()).decode()

    db_token = RefreshToken(
        token = hashed,
        user_id= user_id,
        expires_at= datetime.now(timezone.utc)+ timedelta(days=int(config.REFRESH_TOKEN_EXPIRE_DAYS))
    )

    db.add(db_token)
    db.commit()

    return token

def refresh_token(user_id:int,refresh_token:str, db:Session)->dict:

    tokens= (db.query(RefreshToken)
             .filter(RefreshToken.revoked==False, RefreshToken.user_id==user_id)
             .all()
             )

    token_find = None

    for token in tokens:
        if bcrypt.checkpw(refresh_token.encode(), token.token.encode()):
            token_find = token
            break

    if not token_find:
        raise HTTPException(status_code=401, detail="Refresh token invalido")

    if token_find.expires_at< datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expirado")

    token_find.revoked=True
    db.commit()

    statement = select(User.rol).where(User.id==token_find.user_id)
    role = db.execute(statement).scalar()

    new_access_token = create_access_token(data={
        "id": token_find.user_id,
        "role": role
    })

    new_refresh_token= create_refresh_token(token_find.user_id, db)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }

async def google_info(request:Request)-> dict :
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info= token.get("userinfo")

        return user_info

    except Exception as e:
        raise {"error": str(e)}