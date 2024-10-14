from datetime import datetime
from typing import Optional

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import ReferralCode, User
from app.schemas.referral_code_schema import ReferralCodeBase, ReferralCodeCreate


async def create_code(
    session: AsyncSession, code_data: ReferralCodeCreate, current_user: User
) -> ReferralCode:
    new_code = ReferralCode(**code_data.model_dump())
    new_code.user_id = current_user.id
    session.add(new_code)
    await session.commit()
    return new_code


async def get_referral_code(
    session: AsyncSession, referral_code: ReferralCodeBase
) -> Optional[ReferralCode]:
    query = (
        select(ReferralCode)
        .filter(ReferralCode.code == referral_code)
        .options(selectinload(ReferralCode.user))
    )
    result = await session.execute(query)
    return result.scalar()


async def get_paginated_codes(
    session: AsyncSession, params: Params, current_user: User
) -> Page[ReferralCode]:
    query = select(ReferralCode).filter_by(user_id=current_user.id)
    return await paginate(session, query, params)


async def check_code_unique(
    session: AsyncSession, referral_code: ReferralCodeBase
) -> Optional[ReferralCode]:
    query = select(ReferralCode).filter_by(code=referral_code.code)
    result = await session.execute(query)
    return result.scalar()


async def get_only_active_code(
    session: AsyncSession, user: User
) -> Optional[ReferralCode]:
    query = select(ReferralCode).where(
        ReferralCode.user_id == user.id,
        ReferralCode.expires_at > datetime.now(),
    )
    result = await session.execute(query)
    return result.scalar()


async def delete_referral_code(session: AsyncSession, code: ReferralCode) -> None:
    await session.delete(code)
    await session.commit()
