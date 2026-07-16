import hashlib
import hmac

from app.config import settings


def verify_signature(raw_body: bytes, signature_header: str) -> bool:
    """
    X-Chatwoot-Signature 헤더 형식: "sha256=<hex>"
    시크릿이 비어 있으면(로컬 개발 초기) 검증을 건너뛴다 — 배포 전 반드시 설정할 것.
    """
    if not settings.AGENT_BOT_WEBHOOK_SECRET:
        return True

    if not signature_header or not signature_header.startswith("sha256="):
        return False

    expected = hmac.new(
        settings.AGENT_BOT_WEBHOOK_SECRET.encode("utf-8"),
        raw_body,
        hashlib.sha256,
    ).hexdigest()

    received = signature_header.removeprefix("sha256=")
    return hmac.compare_digest(expected, received)
