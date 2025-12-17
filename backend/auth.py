from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import models
from database import get_db

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

def verify_password(plain_password, hashed_password):
    # Convert to bytes if needed
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password, hashed_password)

def get_password_hash(password):
    # Convert to bytes if needed
    if isinstance(password, str):
        password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed.decode('utf-8')  # Store as string in database

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(request: Request, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Get token from cookie
    token = request.cookies.get("access_token")
    print(f"🔍 Cookies received: {request.cookies}")
    print(f"🔍 Token from cookie: {token}")
    
    if not token:
        print("❌ No token found in cookies")
        raise credentials_exception
    
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token[7:]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            print("❌ No username in token payload")
            raise credentials_exception
        print(f"✅ Token validated for user: {username}")
    except JWTError as e:
        print(f"❌ JWT Error: {e}")
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        print(f"❌ User not found in database: {username}")
        raise credentials_exception
    return user


def get_current_user_optional(request: Request, db: Session = Depends(get_db)):
    """
    Optional authentication - returns User if authenticated, None if not
    Allows anonymous access without raising exceptions
    """
    # Get token from cookie
    token = request.cookies.get("access_token")
    
    if not token:
        return None
    
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token[7:]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        
        user = db.query(models.User).filter(models.User.username == username).first()
        return user
    except JWTError:
        return None
