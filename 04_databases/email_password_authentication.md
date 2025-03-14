# **JWT Authentication in FastAPI**  

## **1. Install Dependencies**  
Ensure you have FastAPI and PyJWT installed:  
```bash
pip install fastapi[all] pyjwt python-multipart passlib
```

---

## **2. Project Structure**  
```
/fastapi_jwt_auth
│── main.py
│── auth.py
│── models.py
│── database.py
│── users.py
│── config.py
```

---

## **3. Configure JWT in `config.py`**
```python
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

---

## **4. Database Setup (`database.py`)**  
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"  # Use PostgreSQL/MySQL for production
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## **5. User Model (`models.py`)**  
```python
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
```

---

## **6. Authentication Logic (`auth.py`)**  
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.password):
        return False
    return user

def get_current_user(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username)
    if user is None:
        raise credentials_exception
    return user
```

---

## **7. User Routes (`users.py`)**  
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import hash_password, authenticate_user, create_access_token
import config

router = APIRouter()

@router.post("/register")
def register_user(username: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = User(username=username, password=hash_password(password))
    db.add(new_user)
    db.commit()
    return {"msg": "User created successfully"}

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

---

## **8. Protect Routes in `main.py`**
```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from auth import get_current_user
import users

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome {current_user.username}"}

# Include user routes
app.include_router(users.router)
```

---

## **9. Testing the API**  

### **Register a User**
```bash
curl -X 'POST' 'http://127.0.0.1:8000/register' -H 'Content-Type: application/json' -d '{"username": "testuser", "password": "testpass"}'
```

### **Login to Get JWT Token**
```bash
curl -X 'POST' 'http://127.0.0.1:8000/login' -H 'Content-Type: application/json' -d '{"username": "testuser", "password": "testpass"}'
```

### **Access Protected Route**
Use the token received from the login API.
```bash
curl -X 'GET' 'http://127.0.0.1:8000/protected' -H 'Authorization: Bearer <your_token>'
```

---

