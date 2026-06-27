from pydantic import BaseModel, ConfigDict


class RegisterUser(BaseModel):
    email: str
    full_name:str
    picture:str
    model_config = ConfigDict(from_attributes=True)