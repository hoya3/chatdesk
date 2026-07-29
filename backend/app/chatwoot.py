import hashlib
import hmac

from app.config import settings


def make_identifier_hash(identifier: str) -> str:
    """
    Chatwoot 위젯 setUser()의 identifier_hash 값을 생성한다.
    이 함수는 반드시 서버에서만 호출한다 — CHATWOOT_HMAC_SECRET이
    브라우저(프론트엔드)로 전달되면 신원 위조가 가능해진다.
    """
    if not settings.CHATWOOT_HMAC_SECRET:
        raise RuntimeError("CHATWOOT_HMAC_SECRET이 설정되지 않았습니다 (.env 확인)")

    return hmac.new(
        settings.CHATWOOT_HMAC_SECRET.encode("utf-8"),
        identifier.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
