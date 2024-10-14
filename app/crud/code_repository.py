from datetime import datetime
from typing import Optional


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


async def check_code_unique(
    session: AsyncSession, referral_code: ReferralCodeBase
) -> Optional[ReferralCode]:
    query = select(ReferralCode).filter_by(code=referral_code.code)
    result = await session.execute(query)
    return result.scalar()


async def check_only_active_code(
    session: AsyncSession, current_user: User
) -> Optional[ReferralCode]:
    query = select(ReferralCode).where(
        ReferralCode.user_id == current_user.id,
        ReferralCode.expires_at > datetime.now(),
    )
    result = await session.execute(query)
    return result.scalar()
