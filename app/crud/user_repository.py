from typing import Optional
from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import EmailStr
from sqlalchemy import or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import ReferralCode, User, user_referral
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


async def create_new_user(session: AsyncSession, user_data: UserCreate) -> User:
    new_user = User(**user_data.model_dump())
    session.add(new_user)
    await session.commit()
    return new_user


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


async def get_referrals_by_referrer(
    session: AsyncSession, params: Params, referrer_id: UUID
) -> Page[User]:
    stmt = select(User).join(User.referrals).where(User.id == referrer_id)
    return await paginate(session, stmt, params)
