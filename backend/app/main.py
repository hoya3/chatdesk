from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth

# 개발 편의용: 최초 실행 시 테이블 자동 생성
# (이전 사용 예정 없음. Alembic 마이그레이션으로 교체 권장)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="상담 채팅 인증 서버")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시 방문자 웹사이트 도메인으로 제한할 것
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/health")
def health():
    return {"status": "ok"}
