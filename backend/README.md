# 인증 서버 (백엔드)

방문자 웹사이트의 회원가입/로그인을 처리하고, 로그인 성공 시
Chatwoot 위젯 `setUser()`에 넘길 HMAC(identifier_hash)까지 함께 발급한다.
Chatwoot 자체 DB와는 완전히 분리된 별도 PostgreSQL을 쓴다.

## 로컬 실행

```bash
cp .env.example .env
# JWT_SECRET, CHATWOOT_HMAC_SECRET 채우기
# (CHATWOOT_HMAC_SECRET은 Chatwoot 인박스 설정 > Identity Validation 에서 복사)

pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 엔드포인트

| Method | Path | 설명 |
|---|---|---|
| POST | `/signup` | 회원가입 |
| POST | `/login` | 로그인 → JWT + chatwoot 식별 정보(identifier, identifier_hash) 반환 |
| GET | `/me` | JWT로 현재 사용자 확인 (새로고침 시 세션 복구용) |

## 파일 구성

- `app/main.py` — FastAPI 앱, CORS
- `app/config.py` — 환경변수
- `app/database.py` — SQLAlchemy 엔진/세션
- `app/models.py` — User 테이블
- `app/auth.py` — 비밀번호 해싱, JWT 발급/검증
- `app/chatwoot.py` — HMAC 계산 (서버 전용, 절대 프론트 노출 금지)
- `app/routers/auth.py` — signup/login/me 라우터

## TODO

- [ ] Alembic 마이그레이션 도입 (지금은 `Base.metadata.create_all`로 자동 생성)
- [ ] `main.py`의 CORS `allow_origins`를 실제 방문자 웹사이트 도메인으로 제한
- [ ] refresh token, 이메일 인증, 비밀번호 재설정 (5주 일정에는 이번 스코프 제외)
