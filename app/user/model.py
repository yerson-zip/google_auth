from sqlalchemy import Column, String, Integer, TIMESTAMP, text
from app.core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    picture = Column(String, nullable=True)
    rol = Column(String, server_default=text("'user'"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))