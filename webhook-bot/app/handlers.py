from app.chatwoot_client import chatwoot_client

# PoC 수준 키워드 매칭. 5주차에 LLM 연동으로 교체 예정.
FAQ = {
    "영업시간": "평일 09:00~18:00 운영합니다.",
    "가격": "요금제는 상담사 연결 후 자세히 도와드리겠습니다.",
    "환불": "환불 규정은 상담사가 직접 확인해드리겠습니다.",
}

# 사용자가 이 표현을 쓰면 곧바로 실제 상담사에게 넘긴다.
HANDOFF_TRIGGERS = ["상담원", "사람과 상담", "직접 상담"]


async def handle_widget_triggered(payload: dict) -> None:
    conversation = payload.get("current_conversation") or payload.get("conversation")
    if not conversation:
        return
    conversation_id = conversation["id"]
    await chatwoot_client.send_message(
        conversation_id,
        "안녕하세요! 무엇을 도와드릴까요? (영업시간 / 가격 / 환불 등을 입력해보세요)",
    )


async def handle_message_created(payload: dict) -> None:
    # 상담사가 보낸 메시지(outgoing)나 봇 자신이 보낸 메시지는 무시
    if payload.get("message_type") != "incoming":
        return

    content = (payload.get("content") or "").strip()
    conversation = payload.get("conversation") or {}
    conversation_id = conversation.get("id")
    if not conversation_id:
        return

    if any(trigger in content for trigger in HANDOFF_TRIGGERS):
        await chatwoot_client.send_message(conversation_id, "상담사에게 연결해드릴게요. 잠시만 기다려주세요.")
        await chatwoot_client.handoff_to_agent(conversation_id)
        return

    for keyword, answer in FAQ.items():
        if keyword in content:
            await chatwoot_client.send_message(conversation_id, answer)
            return

    # 매칭 실패 시 기본 응답 (반복되면 트리아지 로직 고도화 지시 → 4주차 예정)
    await chatwoot_client.send_message(
        conversation_id,
        "죄송해요, 아직 이해하지 못했어요. '상담원 연결'이라고 입력하시면 실제 상담사와 연결됩니다.",
    )
