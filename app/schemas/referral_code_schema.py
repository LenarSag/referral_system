from datetime import datetime
from uuid import UUID

from fastapi.exceptions import ValidationException
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.user_schema import UserOut
from config import CODE_REGEX


class ReferralCodeBase(BaseModel):
    code: str = Field(..., pattern=CODE_REGEX, description='Referral code')


class ReferralCodeCreate(ReferralCodeBase):
    expires_at: datetime

    @field_validator('expires_at')
    @classmethod
    def validate_expires_at(cls, expires_at):
        if expires_at:
            if expires_at < datetime.now():
                raise ValidationException('Expires time less than current time')

        return expires_at


class ReferralCodeOut(BaseModel):
    id: int = Field(..., description='Code id')
    user_id: UUID = Field(..., description='User id')
    code: str = Field(..., description='Referral code')
    expires_at: datetime = Field(..., description='Date and time of expiration')
    is_active: bool = Field(..., description='Active code or not')

    model_config = ConfigDict(from_attributes=True)


class ReferralCodeUserOut(ReferralCodeOut):
    user: UserOut
