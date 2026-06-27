from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.user.model import User
from app.auth.schemas import RegisterUser


error_400 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="credenciales invalidas"
)

def create_user(db:Session, user_request:RegisterUser)->User | None:
    user_db = User(**user_request.model_dump())

    try:
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return user_db
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email existente"
            )


def get_user_by_email(db:Session, email:str)-> type[User]:

    user = db.query(User).filter(User.email==email).first()

    if user is None:
        raise error_400

    return user

def get_user_by_id(db:Session, id:int)->type[User]:
    user = db.query(User).filter(User.id==id).first()

    if user is None:
        raise error_400

    return user