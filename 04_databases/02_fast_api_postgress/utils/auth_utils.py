from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer,APIKeyHeader
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt
import os


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
API_KEY_NAME = "x-api-key"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)


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
    
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        if decoded_token:
            return decoded_token
        else:
            return HTTPException(status_code=401, detail="Token not parseable")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print('An exception occurred')
        print(e)
        return HTTPException(status_code=401, detail="Invalid token")
    

def verify_api_key(api_key_header: str = Depends(api_key_header)):
    try:
        # query api keys table to check if api key exists and is active, and userid match the one in the token
        # db_api_key = get_api_key(userId)
        if api_key_header == os.getenv("API_KEY"):
            return api_key_header
        else:
            raise HTTPException(status_code=401, detail="Invalid API Key")
    except Exception as e:
      print('An exception occurred',e)
      raise HTTPException(status_code=401, detail="Invalid API Key")
    