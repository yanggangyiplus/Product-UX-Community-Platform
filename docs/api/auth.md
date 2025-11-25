# 인증 API

## POST /api/auth/login

일반 로그인 (이메일/비밀번호)

### 요청

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### 응답

**성공 (200)**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "nickname": "사용자",
    "role": "user"
  }
}
```

**실패 (401)**
```json
{
  "error": "이메일 또는 비밀번호가 올바르지 않습니다."
}
```

## GET /api/auth/oauth/{provider}

OAuth 로그인 URL 요청

### 경로 파라미터

- `provider` (string, required): kakao, naver, google 중 하나

### 요청 예시

```http
GET /api/auth/oauth/kakao
```

### 응답

**성공 (200)**
```json
{
  "auth_url": "https://kauth.kakao.com/oauth/authorize?client_id=..."
}
```

## GET /api/auth/callback/{provider}

OAuth 콜백 처리

### 경로 파라미터

- `provider` (string, required): kakao, naver, google 중 하나

### 쿼리 파라미터

- `code` (string, required): OAuth 인증 코드
- `state` (string, optional): 상태값 (네이버/구글)

### 응답

프론트엔드로 리다이렉트:
```
http://localhost:3000/auth/callback?token=<jwt_token>&provider=<provider>
```

