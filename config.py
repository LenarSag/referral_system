import re


SECRET_KEY = 'b0a3f260fecdc69160d4045c276c28fe99bb78a29bf140075b4766b6931b20b0'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30


API_URL = '/api/v1'

EMAILHUNTER_API = 'fake_api'

CODE_REGEX = re.compile(
    r'(?=.*[A-Z])'  # At least one uppercase letter
    r'(?=.*\d)'  # At least one digit
    r'[A-Za-z\d]{12,}$'  # Minimum 12 characters (only letters and digits)
)
