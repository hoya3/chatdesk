import os


class Settings:
    # 팀 인증 서버 자체 DB (Chatwoot DB와는 완전 별도)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://auth_user:auth_pass@auth-db:5432/auth_db"
    )

    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me-in-env")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

    # Chatwoot 인박스 설정 > Identity Validation 에서 복사한 값
    # 절대 프론트엔드에 노출하면 안됨 (서버에서만 사용)
    CHATWOOT_HMAC_SECRET: str = os.getenv("CHATWOOT_HMAC_SECRET", "")


settings = Settings()
