import os


class Settings:
    # Chatwoot Application API 호출용 (메시지 전송, 대화 상태 변경)
    CHATWOOT_BASE_URL: str = os.getenv("CHATWOOT_BASE_URL", "http://localhost:3000")
    CHATWOOT_ACCOUNT_ID: str = os.getenv("CHATWOOT_ACCOUNT_ID", "1")
    CHATWOOT_API_ACCESS_TOKEN: str = os.getenv("CHATWOOT_API_ACCESS_TOKEN", "")

    # Settings > Bots 에서 봇 생성 시 발급되는 secret
    # (웹훅 페이로드 검증용, X-Chatwoot-Signature 헤더와 대조)
    AGENT_BOT_WEBHOOK_SECRET: str = os.getenv("AGENT_BOT_WEBHOOK_SECRET", "")


settings = Settings()
