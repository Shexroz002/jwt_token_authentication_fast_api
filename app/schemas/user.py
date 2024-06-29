# Description: User and Token schemas for the application.
import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    username: str = Field(..., title="The username of the user")
    password: str = Field(..., title="The password of the user")


class User(BaseModel):
    username: str = Field(..., title="The username of the user")
    password: str = Field(..., title="The password of the user")


class Token(BaseModel):
    access_token: str = Field(..., title="The access token of the user")
    token_type: str = Field(..., title="The token type of the user")


class ResponseToken(BaseModel):
    access_token: str = Field(..., title="The access token of the user")


class DataToken(BaseModel):
    id: Optional[str] = None


class UserOutput(BaseModel):
    id: int
    username: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True
