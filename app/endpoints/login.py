from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.code_repository import get_referral_code_from_cache
from app.crud.user_repository import (
    check_username_and_email,
    create_new_referral_user,
    create_new_user,
)
from app.db.database import get_session

from app.schemas.fastapi_models import Token
from app.schemas.user_schema import UserAuthentication, UserCreate, UserOut
from app.security.authentication import authenticate_user, create_access_token
from app.security.pwd_crypt import get_hashed_password
from app.utils.emailhunter import verify_email_with_hunter


loginrouter = APIRouter()


@loginrouter.post('/user', response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    # checks if referral code exists
    if user_data.code:
        referral_code = await get_referral_code_from_cache(session, user_data.code)
        if referral_code is None or not referral_code.is_active:
            raise HTTPException(
                detail='Referral code not found or expired',
                status_code=status.HTTP_404_NOT_FOUND,
            )

    # checks email with Emailhunter
    email_valid = await verify_email_with_hunter(user_data.email)
    if not email_valid:
        print('Fake message: email is not valid!')

    # checks if user with same username or email already exists
    user = await check_username_and_email(session, user_data.username, user_data.email)
    if user:
        if user.username == user_data.username:
            raise HTTPException(
                detail='Username already taken',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        raise HTTPException(
            detail='Email already registered',
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    user_data.password = get_hashed_password(user_data.password)

    # if user registering as follower create referral user
    if user_data.code:
        new_user = await create_new_referral_user(session, user_data, referral_code)
    else:
        new_user = await create_new_user(session, user_data)

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
