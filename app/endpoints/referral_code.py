from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi_pagination import Page, Params
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.code_repository import (
    check_code_unique,
    get_only_active_code,
    create_code,
    delete_referral_code,
    get_paginated_codes,
    get_referral_code,
)
from app.crud.user_repository import get_user_by_email
from app.db.database import get_session
from app.models.user import User
from app.schemas.referral_code_schema import (
    ReferralCodeBase,
    ReferralCodeCreate,
    ReferralCodeOut,
    ReferralCodeUserOut,
)
from app.security.authentication import get_current_user


coderouter = APIRouter()


@coderouter.get('/', response_model=Page[ReferralCodeOut])
async def get_my_referral_codes(
    params: Annotated[Params, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    result = await get_paginated_codes(session, params, current_user)
    return result


@coderouter.get('/{email}', response_model=ReferralCodeUserOut)
async def get_referral_code_from_email(
    email: EmailStr,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    user_with_code = await get_user_by_email(session, email)
    if user_with_code is None:
        raise HTTPException(
            detail='Email not found.',
            status_code=status.HTTP_404_NOT_FOUND,
        )

    referral_code = await get_only_active_code(session, user_with_code)
    if referral_code is None:
        raise HTTPException(
            detail="User doesn't have active codes.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    referral_code_out = ReferralCodeUserOut(
        id=referral_code.id,
        code=referral_code.code,
        expires_at=referral_code.expires_at,
        is_active=referral_code.is_active,
        user=user_with_code,
    )
    return referral_code_out


@coderouter.post(
    '/', response_model=ReferralCodeOut, status_code=status.HTTP_201_CREATED
)
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

    existing_active_code = await get_only_active_code(session, current_user)
    if existing_active_code:
        raise HTTPException(
            detail='You can have only one active code!',
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    new_code = await create_code(session, code_data, current_user)
    return new_code


@coderouter.delete('/{code}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_referral_code(
    code: ReferralCodeBase,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    code_to_delete = await get_referral_code(session, code)
    if code_to_delete is None:
        raise HTTPException(
            detail='Code not found!',
            status_code=status.HTTP_404_NOT_FOUND,
        )
    if code_to_delete.user_id != current_user.id:
        raise HTTPException(
            detail='You can delete only your codes!',
            status_code=status.HTTP_403_FORBIDDEN,
        )

    await delete_referral_code(session, code_to_delete)
