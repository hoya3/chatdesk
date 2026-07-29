from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, decode_access_token, hash_password, verify_password
from app.chatwoot import make_identifier_hash
from app.database import get_db
from app.models import User
from app.schemas import (
    ChatwootIdentity,
    LoginRequest,
    LoginResponse,
    MeResponse,
    SignupRequest,
    UserOut,
)

router = APIRouter(tags=["auth"])


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다")

    user = User(
        email=payload.email,
        name=payload.name,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut(id=str(user.id), email=user.email, name=user.name)


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다")

    identifier = str(user.id)
    token = create_access_token(identifier)

    return LoginResponse(
        access_token=token,
        chatwoot=ChatwootIdentity(
            identifier=identifier,
            identifier_hash=make_identifier_hash(identifier),
            email=user.email,
            name=user.name,
        ),
    )


@router.get("/me", response_model=MeResponse)
def me(user_id: str = Depends(decode_access_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    identifier = str(user.id)
    return MeResponse(
        user=UserOut(id=identifier, email=user.email, name=user.name),
        chatwoot=ChatwootIdentity(
            identifier=identifier,
            identifier_hash=make_identifier_hash(identifier),
            email=user.email,
            name=user.name,
        ),
    )
