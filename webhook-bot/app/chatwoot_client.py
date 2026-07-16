import httpx

from app.config import settings


class ChatwootClient:
    def __init__(self):
        self.base = f"{settings.CHATWOOT_BASE_URL}/api/v1/accounts/{settings.CHATWOOT_ACCOUNT_ID}"
        self.headers = {
            "api_access_token": settings.CHATWOOT_API_ACCESS_TOKEN,
            "Content-Type": "application/json",
        }

    async def send_message(self, conversation_id: int, content: str) -> None:
        url = f"{self.base}/conversations/{conversation_id}/messages"
        payload = {"content": content, "message_type": "outgoing"}
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=self.headers, timeout=10)
            resp.raise_for_status()

    async def handoff_to_agent(self, conversation_id: int) -> None:
        """봇이 해결 불가로 판단했을 때 실제 상담사에게 넘긴다 (pending -> open)."""
        url = f"{self.base}/conversations/{conversation_id}/toggle_status"
        payload = {"status": "open"}
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=self.headers, timeout=10)
            resp.raise_for_status()


chatwoot_client = ChatwootClient()
