# 인증 서버 (백엔드)

방문자 웹사이트의 회원가입/로그인을 처리하고, 로그인 성공 시
Chatwoot 위젯 `setUser()`에 넘길 HMAC(`identifier_hash`)까지 함께 발급한다.
Chatwoot 자체 DB와는 완전히 분리된 SQLite 파일을 쓴다 (별도 DB 컨테이너 불필요).

## 로컬 실행

```bash
cp .env.example .env
# JWT_SECRET, CHATWOOT_HMAC_SECRET 채우기
# (CHATWOOT_HMAC_SECRET은 Chatwoot 인박스 설정 > Identity Validation 에서 복사)

pip install -r requirements.txt
uvicorn app.main:app --reload
# http://localhost:8000/docs 에서 Swagger UI 확인 가능
```

## Docker 실행

```bash
# 루트 디렉터리에서
docker compose up -d --build backend
```

## 환경변수 (`.env.example` 참고)

| 변수 | 설명 | 기본값 |
|---|---|---|
| `DATABASE_URL` | SQLite 파일 경로 | `sqlite:////data/auth.db` |
| `JWT_SECRET` | JWT 서명용 비밀 키 (충분히 긴 랜덤 문자열) | — |
| `JWT_EXPIRE_MINUTES` | 액세스 토큰 유효 시간(분) | `60` |
| `CHATWOOT_HMAC_SECRET` | Chatwoot 인박스 > Identity Validation 토큰 | — |

## 엔드포인트

| Method | Path | 설명 | 인증 |
|---|---|---|---|
| POST | `/signup` | 회원가입 → `UserOut` 반환 | 불필요 |
| POST | `/login` | 로그인 → JWT + Chatwoot 식별 정보 반환 | 불필요 |
| GET | `/me` | JWT로 현재 사용자 확인 (새로고침 세션 복구) | Bearer 토큰 |
| GET | `/health` | 헬스체크 | 불필요 |

### 응답 스키마

**`POST /signup`** → `UserOut`
```json
{ "id": "uuid", "email": "user@example.com", "name": "홍길동" }
```

**`POST /login`** → `LoginResponse`
```json
{
  "access_token": "<JWT>",
  "token_type": "bearer",
  "chatwoot": {
    "identifier": "uuid",
    "identifier_hash": "<HMAC-SHA256>",
    "email": "user@example.com",
    "name": "홍길동"
  }
}
```

**`GET /me`** → `MeResponse`
```json
{
  "user": { "id": "uuid", "email": "user@example.com", "name": "홍길동" },
  "chatwoot": {
    "identifier": "uuid",
    "identifier_hash": "<HMAC-SHA256>",
    "email": "user@example.com",
    "name": "홍길동"
  }
}
```

## 파일 구성

| 파일 | 역할 |
|---|---|
| `app/main.py` | FastAPI 앱 생성, CORS 미들웨어, 라우터 등록 |
| `app/config.py` | 환경변수 로딩 (`Settings`) |
| `app/database.py` | SQLAlchemy 엔진/세션 |
| `app/models.py` | `User` 테이블 정의 |
| `app/schemas.py` | Pydantic 요청/응답 스키마 |
| `app/auth.py` | 비밀번호 해싱(bcrypt), JWT 발급/검증 |
| `app/chatwoot.py` | HMAC 계산 — **절대 프론트 노출 금지** |
| `app/routers/auth.py` | `/signup` `/login` `/me` 라우터 |

## 주요 패키지

| 패키지 | 버전 | 용도 |
|---|---|---|
| `fastapi` | 0.115.6 | 웹 프레임워크 |
| `uvicorn[standard]` | 0.32.1 | ASGI 서버 |
| `sqlalchemy` | 2.0.36 | ORM |
| `passlib[bcrypt]` + `bcrypt` | 1.7.4 / 4.0.1 | 비밀번호 해싱 |
| `python-jose[cryptography]` | 3.3.0 | JWT |
| `pydantic[email]` | 2.10.3 | 요청/응답 검증 |
| `python-dotenv` | 1.0.1 | `.env` 로딩 |

## TODO

- [ ] Alembic 마이그레이션 도입 (현재는 `Base.metadata.create_all`로 자동 생성)
- [ ] `main.py`의 CORS `allow_origins`를 실제 방문자 웹사이트 도메인으로 제한
- [ ] refresh token, 이메일 인증, 비밀번호 재설정 (5주 일정 스코프 외)
