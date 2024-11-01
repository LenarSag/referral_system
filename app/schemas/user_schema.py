import re
from typing import Optional
from uuid import UUID

from fastapi.exceptions import ValidationException
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from config import CODE_REGEX, EMAIL_LENGTH, USERNAME_LENGTH


class UserAuthentication(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str = Field(max_length=USERNAME_LENGTH, pattern=r'^[\w.@+-]+$')
    email: EmailStr = Field(max_length=EMAIL_LENGTH)
    password: str
    code: Optional[str] = Field(None, pattern=CODE_REGEX)

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        password_regex = re.compile(
            r'^'
            r'(?=.*[a-z])'
            r'(?=.*[A-Z])'
            r'(?=.*\d)'
            r'(?=.*[@$!%*?&])'
            r'[A-Za-z\d@$!%*?&]'
            r'{8,}$'
        )
        if not password_regex.match(value):
            raise ValidationException(
                'The length at least 8 symbols, including '
                'lower-case, upper-case, nums, '
                'and special symbols.'
            )
        return value


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserReferrals(UserOut):
    referrals: list[UserOut]
