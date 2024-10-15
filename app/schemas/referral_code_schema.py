from datetime import datetime
from uuid import UUID

from fastapi.exceptions import ValidationException
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.user_schema import UserOut
from config import CODE_REGEX


class ReferralCodeBase(BaseModel):
    code: str = Field(pattern=CODE_REGEX)


class ReferralCodeCreate(ReferralCodeBase):
    expires_at: datetime

    @field_validator('expires_at')
    @classmethod
    def validate_expires_at(cls, expires_at):
        if expires_at:
            if expires_at < datetime.now():
                raise ValidationException(
                    'Expires time less than current time'
                )

        return expires_at


class ReferralCodeOut(BaseModel):
    id: int
    user_id: UUID
    code: str
    expires_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ReferralCodeUserOut(ReferralCodeOut):
    user: UserOut
