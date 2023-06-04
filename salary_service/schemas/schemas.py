from uuid import UUID
from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field, validator
from fastapi import HTTPException, status


class TokenSchema(BaseModel):
    access_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserCreate(BaseModel):
    first_name: str = Field(description="user name")
    last_name: str = Field(description="user last name")
    username: str = Field(description="user login")
    password: str = Field(min_length=5, max_length=24, description="user password")


class RegisteredUser(BaseModel):
    first_name: str
    last_name: str
    username: str


class SalaryData(BaseModel):
    username: str
    salary: Optional[int]
    next_increase_date: Optional[datetime]

    @validator("next_increase_date", pre=True)
    def parse_date_type_data(cls, value):
        if isinstance(value, str):
            date = datetime.strptime(value, "%Y-%m-%d")

            if date < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The date must be greater than the current date"
                )
            return date
        return value


class UserOut(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    username: str


class LoggedInUser(UserOut):
    password: str
