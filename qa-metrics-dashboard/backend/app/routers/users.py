from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db, Base, engine
from ..models import User
from ..schemas import UserCreate, UserOut, Token
from ..auth import hash_password, verify_password, create_access_token, require_role
from ..settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/init", response_model=dict)
def init(db: Session = Depends(get_db)):
    Base.metadata.create_all(bind=engine)
    if not db.query(User).filter(User.email == settings.admin_email).first():
        db.add(User(email=settings.admin_email, password_hash=hash_password(settings.admin_password), role="admin"))
    if not db.query(User).filter(User.email == settings.viewer_email).first():
        db.add(User(email=settings.viewer_email, password_hash=hash_password(settings.viewer_password), role="viewer"))
    db.commit()
    return {"status": "ok"}

@router.post("/register", response_model=UserOut, dependencies=[Depends(require_role("admin"))])
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(400, "Email already registered")
    u = User(email=user.email, password_hash=hash_password(user.password), role=user.role)
    db.add(u); db.commit(); db.refresh(u)
    return u

@router.post("/token", response_model=Token)
def login(form: UserCreate, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == form.email).first()
    if not u or not verify_password(form.password, u.password_hash):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token(sub=u.email, role=u.role)
    return {"access_token": token}
