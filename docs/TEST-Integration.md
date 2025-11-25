# 통합 테스트 가이드

## 개요

이 문서는 프론트엔드와 백엔드 간의 통합 테스트 실행 방법을 설명합니다.

## 사전 준비

### 1. 테스트 데이터 생성

```bash
cd backend
python create_test_data.py
```

이 스크립트는 다음 테스트 계정을 생성합니다:
- 일반 사용자: `test@example.com` / `password123`
- 관리자: `admin@example.com` / `admin123`

### 2. 서버 실행

#### Backend 실행

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python app.py
```

백엔드가 `http://localhost:8000`에서 실행되어야 합니다.

#### Frontend 실행 (선택사항)

통합 테스트는 주로 API 테스트이므로 프론트엔드가 실행 중이지 않아도 됩니다.
하지만 OAuth 콜백 플로우 테스트를 위해서는 프론트엔드가 필요합니다.

```bash
cd frontend
npm run dev
```

## 통합 테스트 실행

### Python 스크립트 실행

```bash
cd backend
python tests/integration_test.py
```

### 테스트 항목

1. **서버 상태 확인**
   - 백엔드 서버가 정상적으로 응답하는지 확인

2. **일반 로그인**
   - 이메일/비밀번호 로그인 테스트
   - JWT 토큰 획득 확인

3. **JWT 토큰 헤더 확인**
   - 인증이 필요한 API에 토큰이 자동으로 포함되는지 확인
   - 게시글 작성 API로 검증

4. **게시글 CRUD**
   - CREATE: 게시글 작성
   - READ: 게시글 조회
   - UPDATE: 게시글 수정
   - DELETE: 게시글 삭제

5. **댓글 CRUD**
   - 댓글 작성
   - 댓글 목록 조회
   - 댓글 삭제

6. **신고 API**
   - 신고 생성
   - 중복 신고 방지 확인

7. **관리자 API**
   - 관리자 로그인
   - 회원 목록 조회
   - 신고 목록 조회

8. **OAuth 콜백 플로우**
   - OAuth URL 생성 확인
   - 실제 콜백은 브라우저에서 수동 테스트 필요

## 수동 테스트 시나리오

### OAuth 콜백 플로우 테스트

1. 프론트엔드에서 `/login` 접근
2. "카카오로 시작하기" 버튼 클릭
3. 카카오 인증 페이지로 리다이렉트 확인
4. 카카오 계정으로 로그인 및 승인
5. 콜백 페이지(`/auth/callback`)로 리다이렉트 확인
6. 토큰이 URL 파라미터로 전달되는지 확인
7. 홈 페이지로 자동 리다이렉트되는지 확인
8. localStorage에 토큰이 저장되는지 확인 (브라우저 개발자 도구)

### JWT 토큰 헤더 자동 포함 확인

1. 브라우저 개발자 도구 열기 (F12)
2. Network 탭 열기
3. 로그인 후 API 요청 확인
4. Request Headers에서 `Authorization: Bearer <token>` 확인

### 게시판 CRUD 실제 DB 저장 검증

#### 게시글 작성
1. 로그인 상태에서 `/posts/new` 접근
2. 게시글 작성 후 저장
3. 데이터베이스에서 확인:
   ```sql
   SELECT * FROM posts WHERE title = '작성한 제목';
   ```

#### 게시글 수정
1. 작성한 게시글 수정
2. 데이터베이스에서 확인:
   ```sql
   SELECT * FROM posts WHERE id = <게시글_ID>;
   -- updated_at이 변경되었는지 확인
   ```

#### 게시글 삭제
1. 게시글 삭제
2. 데이터베이스에서 확인:
   ```sql
   SELECT * FROM posts WHERE id = <게시글_ID>;
   -- status가 'DELETED'인지 확인
   ```

### 신고/관리자 API 작동 여부 테스트

#### 신고 생성
1. 게시글 또는 댓글에서 "신고" 클릭
2. 신고 사유 입력 후 제출
3. 데이터베이스에서 확인:
   ```sql
   SELECT * FROM reports WHERE reporter_id = <사용자_ID> ORDER BY created_at DESC LIMIT 1;
   ```

#### 관리자 신고 처리
1. 관리자 계정으로 로그인
2. `/admin/reports` 접근
3. 신고 목록 확인
4. 신고 상태 변경 (처리중 → 완료)
5. 데이터베이스에서 확인:
   ```sql
   SELECT * FROM reports WHERE id = <신고_ID>;
   -- status가 'RESOLVED'이고 processed_by, processed_at이 설정되었는지 확인
   ```

## 테스트 결과 해석

### 성공적인 테스트 결과

```
============================================================
통합 테스트 시작
============================================================

=== 테스트 1: 서버 상태 확인 ===
✓ PASS: 서버 상태 확인
  Status: 200

=== 테스트 2: 일반 로그인 ===
✓ PASS: 일반 로그인
  Token 획득 성공, User ID: 1

...

============================================================
테스트 결과 요약
============================================================
총 테스트: 8
성공: 8
실패: 0
============================================================
```

### 실패한 테스트 해결 방법

#### "서버 상태 확인" 실패
- 백엔드 서버가 실행 중인지 확인
- 포트 8000이 사용 가능한지 확인

#### "일반 로그인" 실패
- `create_test_data.py`가 실행되었는지 확인
- 데이터베이스에 테스트 사용자가 생성되었는지 확인:
  ```sql
  SELECT * FROM users WHERE email = 'test@example.com';
  ```

#### "JWT 토큰 헤더 확인" 실패
- 토큰이 올바르게 생성되었는지 확인
- 환경 변수 `JWT_SECRET_KEY`가 설정되었는지 확인

#### "게시글 CRUD" 실패
- 데이터베이스 연결 확인
- 테이블이 생성되었는지 확인:
  ```sql
  SHOW TABLES;
  ```

#### "관리자 API" 실패
- 관리자 계정이 생성되었는지 확인:
  ```sql
  SELECT * FROM users WHERE role = 'admin';
  ```

## 지속적인 통합 테스트

### CI/CD 파이프라인에 통합

```yaml
# .github/workflows/integration-test.yml 예시
name: Integration Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: test_password
          MYSQL_DATABASE: community_platform
        ports:
          - 3306:3306
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Set up database
        run: |
          cd backend
          python create_test_data.py
      
      - name: Run backend server
        run: |
          cd backend
          python app.py &
        env:
          DB_HOST: localhost
          DB_PORT: 3306
          DB_USER: root
          DB_PASSWORD: test_password
      
      - name: Run integration tests
        run: |
          cd backend
          python tests/integration_test.py
```

## 성능 테스트

### 부하 테스트

```bash
# Apache Bench를 사용한 부하 테스트
ab -n 1000 -c 10 http://localhost:8000/api/posts
```

### 응답 시간 측정

통합 테스트 스크립트에 응답 시간 측정 기능을 추가할 수 있습니다:

```python
import time

start_time = time.time()
response = requests.get(f"{BASE_URL}/posts")
elapsed_time = time.time() - start_time

if elapsed_time > 1.0:  # 1초 이상이면 경고
    self.log(f"응답 시간이 느립니다: {elapsed_time:.2f}초", Colors.YELLOW)
```

## 문제 해결

### 일반적인 문제

1. **포트 충돌**
   - 다른 프로세스가 포트 8000을 사용 중일 수 있음
   - `lsof -i :8000` (Mac/Linux) 또는 `netstat -ano | findstr :8000` (Windows)로 확인

2. **데이터베이스 연결 오류**
   - 데이터베이스가 실행 중인지 확인
   - `.env` 파일의 데이터베이스 설정 확인

3. **CORS 오류**
   - `CORS_ORIGINS` 환경 변수에 올바른 URL이 포함되어 있는지 확인

4. **토큰 만료**
   - 테스트 중 토큰이 만료될 수 있음
   - `JWT_EXPIRATION_DELTA`를 늘리거나 테스트 시간을 단축

## 추가 테스트 시나리오

### 엣지 케이스 테스트

1. **빈 값 테스트**
   - 제목 없이 게시글 작성 시도
   - 빈 댓글 작성 시도

2. **권한 테스트**
   - 다른 사용자의 게시글 수정 시도
   - 일반 사용자가 관리자 API 접근 시도

3. **중복 테스트**
   - 같은 게시글에 중복 좋아요 시도
   - 같은 항목에 중복 신고 시도

4. **대용량 데이터 테스트**
   - 긴 제목/내용 입력
   - 많은 이미지 업로드

## 테스트 커버리지

현재 통합 테스트는 다음을 커버합니다:

- ✅ 인증 (일반 로그인)
- ✅ JWT 토큰 검증
- ✅ 게시글 CRUD
- ✅ 댓글 CRUD
- ✅ 신고 생성 및 중복 방지
- ✅ 관리자 API
- ⚠️ OAuth 콜백 (수동 테스트 필요)

추가로 테스트가 필요한 영역:

- OAuth 전체 플로우 (브라우저 테스트)
- 이미지 업로드
- 페이지네이션
- 검색 기능
- 필터링 기능

