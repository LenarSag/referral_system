from datetime import date, datetime
import re
from typing import Optional
from uuid import UUID

from fastapi.exceptions import ValidationException
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.user_model import UserSex


class UserAuthentication(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=150)
    password: str
    first_name: str = Field(max_length=50, pattern=r"^[\w.@+-]+$")
    last_name: str = Field(max_length=50, pattern=r"^[\w.@+-]+$")
    sex: UserSex
    birth_date: date

    model_config = ConfigDict(use_enum_values=True)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        password_regex = re.compile(
            r"^"
            r"(?=.*[a-z])"
            r"(?=.*[A-Z])"
            r"(?=.*\d)"
            r"(?=.*[@$!%*?&])"
            r"[A-Za-z\d@$!%*?&]"
            r"{8,}$"
        )
        if not password_regex.match(value):
            raise ValidationException(
                "The length at least 8 symbols, including "
                "lower-case, upper-case, nums, "
                "and special symbols."
            )
        return value

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, birth_date):
        today = date.today()
        age = (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )

        if age < 18:
            raise ValidationException("Age must be at least 18 years old.")
        elif age > 100:
            raise ValidationException("Age must not be older than 100 years.")
        return birth_date


class UserBase(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    sex: UserSex
    photo: str
    birth_date: date

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UserWithCoordinates(UserBase):
    location: "LocationBase"


class UserOut(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    sex: UserSex
    photo: str
    age: int
    distance_to: float
    tags: Optional[list["Tag"]]

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class Tag(BaseModel):
    name: str


class LocationBase(BaseModel):
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)
