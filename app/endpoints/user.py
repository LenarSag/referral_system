from typing import Annotated
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi_pagination import Page, Params
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession


from app.crud.user_repository import get_referrals_by_referrer
from app.db.database import get_session
from app.models.user import User
from app.schemas.user_schema import UserOut
from app.security.authentication import get_current_user


userrouter = APIRouter()


@userrouter.get('/{referrer_id}', response_model=Page[UserOut])
async def get_referrer_referrals(
    referrer_id: UUID,
    params: Annotated[Params, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    result = await get_referrals_by_referrer(session, params, referrer_id)
    return result
