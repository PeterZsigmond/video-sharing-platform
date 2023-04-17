from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(min_length = 3, max_length = 100)


class UserCreate(UserBase):
    password: str = Field(min_length = 8, max_length = 100)


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
