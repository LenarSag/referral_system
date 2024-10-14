from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.code_repository import check_code_unique, check_only_active_code
from app.db.database import get_session
from app.models.user import User
from app.schemas.referral_code_schema import ReferralCodeCreate
from app.security.authentication import get_current_user


coderouter = APIRouter()


@coderouter.post('/')
async def create_referral_code(
    code_data: ReferralCodeCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    code = await check_code_unique(session, code_data)
    if code:
        raise HTTPException(
            detail='Referral code should be unique!',
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    existing_active_code = await check_only_active_code(session, current_user)
    if existing_active_code:
        raise HTTPException(
            detail='You can have only one active code!',
            status_code=status.HTTP_400_BAD_REQUEST,
        )
