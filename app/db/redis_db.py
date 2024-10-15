import json

import aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.code_repository import get_referral_code
from app.schemas.referral_code_schema import ReferralCodeOut


redis = None


async def get_redis() -> aioredis.Redis:
    global redis
    if not redis:
        redis = await aioredis.from_url('redis://localhost:6379', decode_responses=True)
    return redis


async def get_referral_code_from_cache(session: AsyncSession, code: str):
    redis = await get_redis()
    cached_referral_code = await redis.get(f'referral:{code}')
    if cached_referral_code:
        return ReferralCodeOut(**json.loads(cached_referral_code))

    referral_code = await get_referral_code(session, code)
    if referral_code:
        referral_code_out = ReferralCodeOut(
            id=referral_code.id,
            user_id=referral_code.user_id,
            code=referral_code.code,
            expires_at=referral_code.expires_at,
            is_active=referral_code.is_active,
        )
        await redis.set(
            f'referral:{code}', referral_code_out.model_dump_json(), ex=3600
        )
        return referral_code_out

    return None
