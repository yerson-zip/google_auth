from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.auth.service import verification_token
from app.core.db import get_db
from app.user.service import get_user_by_id


def get_token(request:Request)->str:
    authorization = request.headers.get("Authorization")

    if not authorization or not authorization.startswith("Beare ") or not verification_token(authorization.split(" ")[1]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return authorization.split(" ")[1]

def get_current_user( db: Session=Depends(get_db), token :str = Depends(get_token)):
    payload = verification_token(token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")

    sub = payload["sub"]

    user = get_user_by_id(db, int(sub))

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

    return user
