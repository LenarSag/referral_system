import asyncio

from fastapi import FastAPI, Request, status
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import uvicorn

from app.db.database import init_models
from app.endpoints.referral_code import coderouter
from app.endpoints.login import loginrouter
from app.endpoints.user import userrouter
from config import API_URL


app = FastAPI()


app.include_router(loginrouter, prefix=f'{API_URL}/auth')
app.include_router(coderouter, prefix=f'{API_URL}/codes')
app.include_router(userrouter, prefix=f'{API_URL}/users')


@app.exception_handler(ValidationError)
async def custom_pydantic_validation_error_handler(
    request: Request, exc: ValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': exc.errors()},
    )


@app.exception_handler(ValidationException)
async def custom_fastapi_validation_error_handler(
    request: Request, exc: ValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': exc.errors()},
    )


if __name__ == '__main__':
    asyncio.run(init_models())
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000, reload=True)
