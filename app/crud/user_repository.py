from typing import Optional

from pydantic import EmailStr
from sqlalchemy import or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import ReferralCode, User, user_referral
from app.schemas.referral_code_schema import ReferralCodeBase
from app.schemas.user_schema import UserCreate


async def check_username_and_email(
    session: AsyncSession, username: str, email: EmailStr
) -> Optional[User]:
    query = select(User).where(or_(User.username == username, User.email == email))
    result = await session.execute(query)
    return result.scalar()


async def get_user_by_email(session: AsyncSession, email: EmailStr) -> Optional[User]:
    query = select(User).filter_by(email=email)
    result = await session.execute(query)
    return result.scalar()


async def get_referral_code(session: AsyncSession, referral_code: ReferralCodeBase):
    query = (
        select(ReferralCode)
        .filter(ReferralCode.code == referral_code)
        .options(selectinload(ReferralCode.user))
    )
    result = await session.execute(query)
    return result.scalar()


async def create_new_referral_user(
    session: AsyncSession, user_data: UserCreate, referrall_code: ReferralCode
) -> User:
    new_user = User(**user_data.model_dump())
    session.add(new_user)
    await session.flush()

    new_referral = {'user_id': referrall_code.user_id, 'user_referral': new_user.id}
    await session.execute(user_referral.insert().values(new_referral))
    await session.commit()

    return new_user
