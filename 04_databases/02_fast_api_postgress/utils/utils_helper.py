from datetime import datetime, timedelta
from typing import Optional
import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try: 
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode,  SECRET_KEY , algorithm=ALGORITHM) # type: ignore
    except Exception as e:
        print('An exception occurred')
        print(e)
        return None
    
def decode_access_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        return decoded_token
    except Exception as e:
        print('An exception occurred')
        print(e)
        return None