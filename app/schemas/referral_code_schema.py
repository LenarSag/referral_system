from datetime import datetime
import re

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user_schema import UserOut


code_regex = re.compile(
    r'^(?=.*[a-z])'  # At least one lowercase letter
    r'(?=.*[A-Z])'  # At least one uppercase letter
    r'(?=.*\d)'  # At least one digit
    r'[A-Za-z\d]{12,}$'  # Minimum 12 characters (only letters and digits)
)


class ReferralCodeBase(BaseModel):
    code: str = Field(pattern=code_regex)


class ReferralCodeCreate(ReferralCodeBase):
    expires_at: datetime
    active: bool


class ReferralCodeOut(ReferralCodeCreate):
    id: int
    user: UserOut

    model_config = ConfigDict(from_attributes=True)
