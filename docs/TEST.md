# 테스트 방법

## 환경 설정

### 1. 데이터베이스 설정

#### MySQL 사용 시

```bash
# MySQL 접속
mysql -u root -p

# 데이터베이스 생성
CREATE DATABASE community_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 사용자 생성 (선택사항)
CREATE USER 'community_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON community_platform.* TO 'community_user'@'localhost';
FLUSH PRIVILEGES;
```

#### PostgreSQL 사용 시

```bash
# PostgreSQL 접속
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE community_platform;
```

### 2. 환경 변수 설정

#### Backend

`backend/.env` 파일 생성:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=community_platform
DB_TYPE=mysql

JWT_SECRET_KEY=your_secret_key_here_change_in_production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DELTA=86400

KAKAO_CLIENT_ID=your_kakao_client_id
KAKAO_CLIENT_SECRET=your_kakao_client_secret
KAKAO_REDIRECT_URI=http://localhost:3000/auth/kakao/callback

NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret
NAVER_REDIRECT_URI=http://localhost:3000/auth/naver/callback

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/google/callback

FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=8000

CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

#### Frontend

`frontend/.env` 파일 생성:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### 3. 의존성 설치

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend

```bash
cd frontend
npm install
```

## 데이터베이스 초기화

### 테이블 생성

```bash
cd backend
python -c "from database import init_db; init_db()"
```

또는 Python 인터프리터에서:

```python
from database import init_db
init_db()
```

## 서버 실행

### Backend 실행

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python app.py
```

백엔드는 `http://localhost:8000`에서 실행됩니다.

### Frontend 실행

```bash
cd frontend
npm run dev
```

프론트엔드는 `http://localhost:3000` (또는 Vite 기본 포트)에서 실행됩니다.

## 테스트 시나리오

### 1. 인증 테스트

#### 일반 로그인

1. 프론트엔드에서 `/login` 접근
2. 이메일과 비밀번호 입력
3. "로그인" 버튼 클릭
4. 토큰이 저장되고 홈으로 리다이렉트되는지 확인

#### 소셜 로그인 (카카오)

1. 프론트엔드에서 `/login` 접근
2. "카카오로 시작하기" 버튼 클릭
3. 카카오 인증 페이지로 리다이렉트되는지 확인
4. 카카오 계정으로 로그인 및 승인
5. 콜백 페이지로 리다이렉트되고 토큰이 저장되는지 확인

### 2. 게시글 테스트

#### 게시글 작성

1. 로그인 상태에서 `/posts/new` 접근
2. 제목과 내용 입력
3. "게시하기" 버튼 클릭
4. 게시글 상세 페이지로 리다이렉트되는지 확인

#### 게시글 목록 조회

1. `/posts` 접근
2. 게시글 목록이 표시되는지 확인
3. 페이지네이션 동작 확인
4. 검색 기능 동작 확인

#### 게시글 상세 조회

1. 게시글 목록에서 게시글 클릭
2. 게시글 상세 내용이 표시되는지 확인
3. 조회수가 증가하는지 확인

#### 게시글 수정/삭제

1. 본인이 작성한 게시글 상세 페이지 접근
2. "수정" 버튼 클릭하여 수정 페이지로 이동
3. 내용 수정 후 저장
4. "삭제" 버튼 클릭하여 삭제 확인

### 3. 댓글 테스트

#### 댓글 작성

1. 게시글 상세 페이지 접근
2. 댓글 입력란에 내용 입력
3. "댓글 작성" 버튼 클릭
4. 댓글이 추가되는지 확인

#### 대댓글 작성

1. 기존 댓글에 대댓글 작성 (추후 구현)
2. 트리 구조로 표시되는지 확인

### 4. 신고 테스트

#### 신고 생성

1. 게시글 또는 댓글에서 "신고" 버튼 클릭
2. 신고 유형 선택 및 사유 입력
3. 신고 제출
4. "신고가 접수되었습니다" 메시지 확인

#### 중복 신고 방지

1. 같은 항목을 다시 신고 시도
2. "이미 신고한 항목입니다" 에러 메시지 확인

### 5. 관리자 테스트

#### 관리자 권한 확인

1. 일반 사용자로 로그인
2. `/admin` 접근 시도
3. 접근 거부되는지 확인

#### 신고 처리

1. 관리자 계정으로 로그인
2. `/admin/reports` 접근
3. 신고 목록 확인
4. 신고 상태 변경 (처리중 → 완료)
5. 처리 사유 입력

#### 회원 관리

1. `/admin/users` 접근
2. 회원 목록 확인
3. 회원 역할 변경 (일반회원 → 관리자)
4. 회원 활성화/비활성화

## API 테스트 (cURL)

### 로그인

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

### 게시글 목록 조회

```bash
curl http://localhost:8000/api/posts?page=1&per_page=20
```

### 게시글 작성 (인증 필요)

```bash
curl -X POST http://localhost:8000/api/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "title": "테스트 게시글",
    "content": "테스트 내용",
    "status": "published"
  }'
```

### 댓글 작성

```bash
curl -X POST http://localhost:8000/api/comments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "post_id": 1,
    "content": "테스트 댓글"
  }'
```

## 문제 해결

### 데이터베이스 연결 오류

- 데이터베이스가 실행 중인지 확인
- `.env` 파일의 데이터베이스 설정 확인
- 데이터베이스 사용자 권한 확인

### CORS 오류

- `backend/.env`의 `CORS_ORIGINS`에 프론트엔드 URL이 포함되어 있는지 확인
- 프론트엔드와 백엔드 포트가 올바른지 확인

### 인증 오류

- JWT 토큰이 올바르게 생성되는지 확인
- 토큰 만료 시간 확인
- `JWT_SECRET_KEY`가 설정되어 있는지 확인

### OAuth 오류

- 각 OAuth 제공자의 클라이언트 ID/Secret이 올바른지 확인
- 리다이렉트 URI가 OAuth 앱 설정과 일치하는지 확인

## 테스트 데이터 생성

### Python 스크립트로 테스트 데이터 생성

`backend/create_test_data.py` 파일 생성:

```python
from database import SessionLocal, init_db
from models import User, Post, Category, UserRole
import hashlib

def create_test_data():
    init_db()
    db = SessionLocal()
    
    try:
        # 테스트 사용자 생성
        user = User(
            email="test@example.com",
            password_hash=hashlib.sha256("password123".encode()).hexdigest(),
            nickname="테스트 사용자",
            role=UserRole.USER
        )
        db.add(user)
        
        # 관리자 사용자 생성
        admin = User(
            email="admin@example.com",
            password_hash=hashlib.sha256("admin123".encode()).hexdigest(),
            nickname="관리자",
            role=UserRole.ADMIN
        )
        db.add(admin)
        
        db.commit()
        print("테스트 데이터가 생성되었습니다.")
    except Exception as e:
        db.rollback()
        print(f"오류 발생: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
```

실행:

```bash
cd backend
python create_test_data.py
```

## 성능 테스트

### 부하 테스트 (선택사항)

Apache Bench를 사용한 간단한 부하 테스트:

```bash
# 게시글 목록 조회 부하 테스트
ab -n 1000 -c 10 http://localhost:8000/api/posts
```

## 보안 테스트

1. **SQL Injection**: 입력값에 SQL 코드 삽입 시도
2. **XSS**: 스크립트 태그 입력 시도
3. **CSRF**: 토큰 없이 요청 시도
4. **권한 우회**: 다른 사용자의 게시글 수정/삭제 시도

