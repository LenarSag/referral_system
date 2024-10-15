from fastapi import status
import httpx
from pydantic import EmailStr

from config import EMAILHUNTER_API


async def verify_email_with_hunter(email: EmailStr) -> bool:
    url = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={EMAILHUNTER_API}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            return data['data']['result'] == 'deliverable'
        return False
