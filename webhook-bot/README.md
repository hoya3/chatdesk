# Agent Bot Webhook 수신 서버

Chatwoot Agent Bot이 보내는 이벤트(`widget_triggered`, `message_created` 등)를 받아
자동응답하거나, 처리 불가 시로 판단되면 실제 상담사에게 넘긴다(트리아지).

## 로컬 실행

```bash
cp .env.example .env
# CHATWOOT_BASE_URL, CHATWOOT_API_ACCESS_TOKEN, AGENT_BOT_WEBHOOK_SECRET 채우기

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

## Chatwoot 쪽 등록

루트 README의 "Agent Bot webhook URL 등록 방법" 참고.

## 동작 확인 (로컬, Chatwoot 없이 curl로만 테스트)

```bash
curl -X POST http://localhost:8001/webhook/agent-bot \
  -H "Content-Type: application/json" \
  -d '{
    "event": "message_created",
    "message_type": "incoming",
    "content": "영업시간이 어떻게 되나요?",
    "conversation": {"id": 1}
  }'
```

(단, 실제로 Chatwoot에 메시지가 전송되려면 `CHATWOOT_API_ACCESS_TOKEN`이 유효해야 함)

## 파일 구성

- `app/main.py` — 웹훅 수신 엔드포인트, 서명 검증, 이벤트 라우팅
- `app/security.py` — X-Chatwoot-Signature 검증
- `app/chatwoot_client.py` — 메시지 전송 / 상태 변경 API 호출
- `app/handlers.py` — 실제 자동응답/트리아지 로직 (현재 키워드 매칭 PoC)

## TODO (4~5주차)

- [ ] `handlers.py`의 키워드 매칭을 LLM 연동으로 교체
- [ ] 대화별 컨텍스트(이전 메시지) 기억 — 지금은 매 메시지 독립 처리
- [ ] 재시도/에러 로깅 강화
