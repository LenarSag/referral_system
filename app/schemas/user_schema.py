import re
from typing import Optional
from uuid import UUID

from fastapi.exceptions import ValidationException
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from config import CODE_REGEX, EMAIL_LENGTH, USERNAME_LENGTH


class UserAuthentication(BaseModel):
    username: str = Field(..., description='Username')
    password: str = Field(..., description='Password')


class UserCreate(BaseModel):
    username: str = Field(
        ..., max_length=USERNAME_LENGTH, pattern=r'^[\w.@+-]+$', description='Username'
    )
    email: EmailStr = Field(..., max_length=EMAIL_LENGTH, description='Email address')
    password: str = Field(..., description='Password')
    code: Optional[str] = Field(None, pattern=CODE_REGEX, description='Referral code')

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
    id: UUID = Field(..., description='User id')
    email: EmailStr = Field(..., description='Email address')
    username: str = Field(..., description='Username')

    model_config = ConfigDict(from_attributes=True)


class UserReferrals(UserOut):
    referrals: list[UserOut]
