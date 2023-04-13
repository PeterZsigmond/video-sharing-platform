from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
