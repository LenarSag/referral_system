from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user_repository import (
    check_username_and_email,
    create_new_referral_user,
    create_new_user,
    get_referral_code,
    get_user_by_email,
    get_user_by_username,
)
from app.db.database import get_session
from app.schemas.fastapi_models import Token
from app.schemas.referral_code_schema import ReferralCodeBase
from app.schemas.user_schema import UserAuthentication, UserCreate, UserOut
from app.security.authentication import authenticate_user, create_access_token
from app.security.pwd_crypt import get_hashed_password


loginrouter = APIRouter()


@loginrouter.post('/user', response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    user = await check_username_and_email(session, user_data.username, user_data.email)
    if user:
        if user.username == user_data.username:
            raise HTTPException(
                detail='Username already taken',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        raise HTTPException(
            detail='Email already registered',
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user_data.password = get_hashed_password(user_data.password)
    new_user = await create_new_user(session, user_data)
    return new_user


@loginrouter.post(
    '/user/{code}',
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_as_referral(
    code: ReferralCodeBase,
    user_data: UserCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    referral_code = await get_referral_code(session, code)
    if referral_code is None:
        raise HTTPException(
            detail='Referral code not found',
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    user = await check_username_and_email(session, user_data.username, user_data.email)
    if user:
        if user.username == user_data.username:
            raise HTTPException(
                detail='Username already taken',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        raise HTTPException(
            detail='Email already registered',
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user_data.password = get_hashed_password(user_data.password)
    new_user = await create_new_referral_user(session, user_data, referral_code)
    return new_user


@loginrouter.post('/token')
async def login_for_access_token(
    form_data: UserAuthentication,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = create_access_token(user)
    return Token(access_token=access_token, token_type='Bearer')
