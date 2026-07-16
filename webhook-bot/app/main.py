import logging

from fastapi import FastAPI, HTTPException, Request

from app.handlers import handle_message_created, handle_widget_triggered
from app.security import verify_signature

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent-bot-webhook")

app = FastAPI(title="Agent Bot Webhook 수신 서버")

EVENT_HANDLERS = {
    "widget_triggered": handle_widget_triggered,
    "message_created": handle_message_created,
}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/webhook/agent-bot")
async def receive_webhook(request: Request):
    raw_body = await request.body()
    signature = request.headers.get("X-Chatwoot-Signature", "")

    if not verify_signature(raw_body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    event = payload.get("event")
    logger.info("event received: %s", event)

    handler = EVENT_HANDLERS.get(event)
    if handler:
        await handler(payload)
    else:
        logger.info("unhandled event type: %s", event)

    return {"ok": True}
