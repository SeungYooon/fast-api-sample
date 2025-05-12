# 📝 Fast Api Sample

FastAPI 기반의 블로그  
회원가입, 로그인, 게시판, 댓글, 관리자 기능

---

## 🔧 사용 기술

| 영역         | 스택                            |
|--------------|---------------------------------|
| Language     | Python 3.11                     |
| Framework    | FastAPI                         |
| ORM          | SQLAlchemy                      |
| DB           | SQLite                          |
| Auth         | JWT (OAuth2PasswordBearer)      |
| Docs         | Swagger (자동 생성)             |

---

## ✅ 주요 기능

### 👤 사용자
- 회원가입 (`POST /users/signup`)
- 로그인 (`POST /users/login`)
- JWT 기반 인증 처리

### 📝 게시글
- 게시글 작성 / 조회 / 수정 / 삭제
- 키워드 검색 (`/posts/search?q=...`)
- 페이징 조회 (`/posts/?skip=0&limit=10`)

### 💬 댓글
- 댓글 작성 / 조회
- 댓글 수정 / 삭제

### 🛡️ 관리자 기능
- 관리자만 가능한 전체 게시글/댓글 조회 및 삭제
- `is_admin` 필드 기반 권한 분리

---

## 🚀 실행 방법

1. 패키지 설치

```bash
pip install -r requirements.txt

### 🌍 배포 링크

- 서비스 주소: [https://fast-api-sample-c2zy.onrender.com](https://fast-api-sample-c2zy.onrender.com)
- Swagger 문서: [https://fast-api-sample-c2zy.onrender.com/docs](https://fast-api-sample-c2zy.onrender.com/docs)

