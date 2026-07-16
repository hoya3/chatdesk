# 웹 상담 채팅 - 팀 자체 개발 서비스 모노레포

Chatwoot(fork, 별도 레포)을 대화하는 팀 자체 신규 개발 3종 모아둔 레포.
Chatwoot 코드는 이 레포에 없다 → Chatwoot fork 레포는 그대로 별도 유지.

```
consultation-chat/
├── frontend/     방문자 웹사이트 (Vue 3 + Vite) — 로그인/회원가입 + Chatwoot 위젯 embed
├── backend/      인증 서버 (FastAPI) — 회원가입/로그인/JWT + HMAC(identifier_hash) 발급
├── webhook-bot/  Agent Bot webhook 수신 서버 (FastAPI) — 자동응답/트리아지
└── docker-compose.yml
```

## 담당 매핑

| 서비스 | 담당 | 오늘 대화에서 다룬 내용 |
|---|---|---|
| frontend | 팀원1 | 로그인/회원가입 UI, 위젯 embed, setUser()/reset() 연동 |
| backend | 본인 | 회원 DB, JWT, HMAC 발급 |
| webhook-bot | 나머지 1명 | Agent Bot 이벤트 수신, 자동응답, 트리아지 |

## 전체 흐름

```
방문자 브라우저
   │  로그인 폼 제출
   ▼
frontend (Vue) ──POST /login──▶ backend (FastAPI)
   │                                 │ JWT + identifier_hash 계산
   ◀──────── access_token + chatwoot{identifier, identifier_hash} ────────┘
   │
   │  window.$chatwoot.setUser(identifier, {identifier_hash, ...})
   ▼
Chatwoot 위젯 (iframe, Chatwoot fork가 서비)
   │
   │  방문자가 메시지 전송 → Chatwoot가 webhook 이벤트 발송
   ▼
webhook-bot ──POST 메시지/상태변경──▶ Chatwoot Application API
```

## 실행 순서

1. Chatwoot fork 레포를 먼저 별도로 띄운다 (`Chatwoot_개발환경_구축_가이드.md` 참고)
2. 이 레포의 각 서비스 `.env.example`을 복사해 `.env`로 만들고 값 채우기
3. `docker network ls`로 Chatwoot 쪽 네트워크 이름 확인 → `docker-compose.yml`의 `chatwoot_default`를 그 이름으로 교체
4. `docker compose up -d --build`

## Agent Bot webhook URL 등록 방법 (webhook-bot 담당자용)

이 레포 코드를 아무리 잘 짜도, **Chatwoot 대시보드에서 등록을 안 하면 이벤트가 안 옵니다.** 순서:

1. `docker compose up`으로 webhook-bot 컨테이너 기동 확인 (`GET /health` 응답 확인)
2. Chatwoot 대시보드 → Settings → Bots → Add Bot
3. Webhook URL을 **`http://webhook-bot:8001/webhook/agent-bot`** 입력
   - `webhook-bot`은 docker-compose 서비스명 → Chatwoot 컨테이너 기준으로 접근 가능한 주소
   - `http://localhost:8001/...`로 입력하면 절대 안됨 (Chatwoot 컨테이너 내장은 localhost는 자기 자신)
4. 봇 생성 시 발급되는 secret을 복사해 `webhook-bot/.env`의 `AGENT_BOT_WEBHOOK_SECRET`에 저장
5. Settings → Inboxes → (해당 인박스) → Bot Configuration에서 방금 만든 봇을 인박스에 연결

## 로컬 개발(Docker 없이 각자 IDE에서 돌릴 때)

Docker 네트워크 없이 실행되므로 서비스명 대신 `localhost:포트`를 그대로 써도 된다.
단, 이 경우 Chatwoot도 로컬에서 같이 떠 있어야 하고 각자 `websiteToken`이 다르다는 점 (팀원마다 로컬 Chatwoot 별개) 주의.

## 스코프에서 뺀 것 (5주 일정 고려)

- frontend: 이메일 인증 화면, 반응형 스타일 다듬기
- backend: refresh token, 이메일 인증, 비밀번호 재설정, Alembic 마이그레이션
- webhook-bot: 지금은 키워드 매칭 PoC. LLM 연동은 4~5주차 예정(각 서비스 README의 TODO 참고)
