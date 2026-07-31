# 웹 실시간 상담 챗 - 팀 자체 개발 서비스 모노레포

Chatwoot(fork, 별도 레포)와 나란히 동작하는 팀 자체 신규 개발 2종을 모아둔 레포입니다.
**Chatwoot 코드는 이 레포에 없습니다** — Chatwoot fork 레포는 별도로 그대로 유지합니다.
**webhook-bot(Agent Bot)은 AI봇 전용 별도 레포로 분리되어 이 레포에서 제거되었습니다.**

```
chatdesk/
├── frontend/     방문자 웹사이트 (Vue 3 + Vite + Pinia + Vue Router) — 로그인/회원가입 + Chatwoot 위젯 embed
├── backend/      인증 서버 (FastAPI) — 회원가입/로그인/JWT + HMAC(identifier_hash) 발급
└── docker-compose.yml
```

## 담당 매핑

| 서비스      | 담당  | 상세 문서                                    |
| ----------- | ----- | --------------------------------------------- |
| `frontend/` | 팀원1 | 이 문서 하단 "브랜치 전략" 참고               |
| `backend/`  | 본인  | [`backend/README.md`](./backend/README.md)   |

각자 자기 폴더의 README부터 읽고 시작하세요.

## 처음 이 레포를 받았다면 (팀원 온보딩)

```bash
git clone <이 레포 주소>
cd chatdesk
git checkout dev
git pull
```

> **Windows에서 작업하는 경우**: 반드시 WSL 안에서 clone하세요. Windows 경로(`/mnt/c/...`)에 두면 파일 I/O가 느려지고, CRLF 줄바꿈이 섞여 git diff가 지저분해집니다.

## 전체 흐름

```
방문자 브라우저
   │  로그인 폼 제출
   ▼
frontend (Vue) ──POST /login──▶ backend (FastAPI)
   │                                 │ JWT + identifier_hash 계산
   │◀─────── access_token + chatwoot{identifier, identifier_hash} ───────┘
   │
   │  window.$chatwoot.setUser(identifier, {identifier_hash, ...})
   ▼
Chatwoot 위젯 (iframe, Chatwoot fork가 서빙)
   │
   │  방문자가 메시지 전송 → Chatwoot가 webhook 이벤트 발송
   ▼
(AI봇 전용 별도 레포) ──POST 메시지/상태변경──▶ Chatwoot Application API
```

## 전체 통합 실행 순서

1. Chatwoot fork 레포를 먼저 별도로 띄운다
2. `docker network ls`로 Chatwoot 쪽 네트워크 이름 확인 → `docker-compose.yml`의 `chatwoot_default`를 그 이름으로 교체
3. 각 서비스 `.env.example`을 복사해 `.env`로 만들고 값 채우기
4. `docker compose up -d --build`

서비스 포트: `frontend` → http://localhost:5173 / `backend` → http://localhost:8000

## 로컬 개발 (Docker 없이 각자 IDE에서 돌릴 때)

Docker 네트워크 밖이므로 `localhost:포트`를 그대로 써도 됩니다. Chatwoot도 로컬에서 같이 떠 있어야 하고, 팀원마다 `websiteToken`이 다르다는 점 주의.

```bash
# frontend (http://localhost:5173)
cd frontend
npm install
npm run dev

# backend (http://localhost:8000 / Swagger: http://localhost:8000/docs)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 브랜치 전략

- `main`: 안정 버전만
- `dev`: 팀 공용 개발 브랜치 — **여기 직접 커밋 금지**
- `feature/서비스명-작업내용`: 실제 작업은 전부 여기서

```bash
git checkout dev && git pull
git checkout -b feature/frontend-login

# 작업 후

git push -u origin feature/frontend-login

# GitHub에서 dev로 PR → 리뷰 → 머지 → 브랜치 삭제
```

## 이번 스프린트 스코프에서 뺀 것 (5주 일정 고려)

- frontend: 이메일 인증 화면, 반응형 스타일
- backend: refresh token, 이메일 인증, 비밀번호 재설정, Alembic 마이그레이션
