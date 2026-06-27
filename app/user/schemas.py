from pydantic import BaseModel, ConfigDict

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    picture: str
    rol: str

    model_config = ConfigDict(from_attributes=True)