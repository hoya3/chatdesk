import uuid

from sqlalchemy import Column, String, DateTime, func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    # 이 id 값이 곧 Chatwoot setUser()의 identifier로 쓰인다
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
