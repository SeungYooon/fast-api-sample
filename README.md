# 📝 FastAPI Sample

FastAPI 기반의 블로그 백엔드 API  
회원가입, 로그인, 게시판, 댓글, 관리자, 비동기 알림 기능 지원

---

## 🔧 사용 기술

| 영역         | 스택                                      |
|--------------|-------------------------------------------|
| Language     | Python 3.11                               |
| Framework    | FastAPI                                   |
| ORM          | SQLAlchemy                                |
| DB           | SQLite                                    |
| Auth         | JWT (OAuth2PasswordBearer)                |
| Docs         | Swagger (자동 생성)                       |
| Async Task   | Celery + Redis                            |
| Search       | Elasticsearch 8                           |
| CI/CD        | GitHub Actions + Render                   |
| Test         | pytest + coverage                         |
| Lint/Format  | pre-commit (black, isort, flake8)         |

---

## ✅ 주요 기능

### 👤 사용자
- 회원가입 (`POST /users/signup`)
- 로그인 (`POST /users/login`)
- JWT 기반 인증 처리

### 📝 게시글
- 게시글 작성 / 조회 / 수정 / 삭제
- 키워드 검색 (`GET /posts/search?q=...`)
- 페이징 조회 (`GET /posts/?skip=0&limit=10`)
- 게시글 작성 시 Elasticsearch 색인 등록 (index: `posts`)

### 💬 댓글
- 댓글 작성 / 조회 / 수정 / 삭제

### 🛡️ 관리자 기능
- 관리자만 가능한 전체 게시글/댓글 조회 및 삭제
- `is_admin` 필드 기반 권한 분리

### 📢 알림 시스템
- 게시글 작성 시 Celery + Redis 기반 비동기 알림 발송
- `send_notification.delay(user_id)`로 작업 큐에 등록

---

## 🚀 실행 방법

### 1. 패키지 설치

```bash
pip install -r requirements.txt
