from datetime import date
from typing import Optional
import uuid


from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy.orm import Query

from app.models.user_model import User, UserSex


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: uuid.UUID
