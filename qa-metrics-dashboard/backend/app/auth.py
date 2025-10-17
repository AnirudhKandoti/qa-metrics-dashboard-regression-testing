from datetime import datetime, timedelta
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

ROLE_ADMIN = "admin"
ROLE_VIEWER = "viewer"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(sub: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode = {"sub": sub, "role": role, "exp": expire}
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_alg)

class UserCtx:
    def __init__(self, email: str, role: str):
        self.email = email
        self.role = role

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> UserCtx:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
        email: str = payload.get("sub")
        role: str = payload.get("role", ROLE_VIEWER)
        if email is None:
            raise ValueError
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return UserCtx(email, role)

def require_role(*roles: str):
    async def checker(user: UserCtx = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return checker
