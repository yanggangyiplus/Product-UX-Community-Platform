# 관리자 API

모든 관리자 API는 관리자 권한(`@admin_required`)이 필요합니다.

## GET /api/admin/reports

신고 목록 조회

**인증 필요 (관리자 권한)**

### 쿼리 파라미터

- `status` (string, optional): 상태 필터
- `page` (int, default: 1)
- `per_page` (int, default: 20)

### 응답

`GET /api/reports`와 동일

## PUT /api/admin/reports/{id}

신고 상태 변경

**인증 필요 (관리자 권한)**

### 요청 본문

```json
{
  "status": "resolved",
  "admin_note": "신고 내용 확인 후 게시글 삭제 처리"
}
```

### 응답

**성공 (200)**
```json
{
  "message": "신고 상태가 변경되었습니다."
}
```

## GET /api/admin/users

회원 목록 조회

**인증 필요 (관리자 권한)**

### 쿼리 파라미터

- `page` (int, default: 1)
- `per_page` (int, default: 20)
- `search` (string, optional): 검색어

### 응답

**성공 (200)**
```json
{
  "users": [
    {
      "id": 1,
      "email": "user@example.com",
      "nickname": "사용자",
      "role": "user",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 100,
  "page": 1,
  "per_page": 20
}
```

## PUT /api/admin/users/{id}

회원 정보 수정

**인증 필요 (관리자 권한)**

### 요청 본문

```json
{
  "is_active": false,
  "role": "admin"
}
```

### 응답

**성공 (200)**
```json
{
  "message": "회원 정보가 수정되었습니다."
}
```

## GET /api/admin/posts

게시글 목록 조회 (관리자용)

**인증 필요 (관리자 권한)**

### 쿼리 파라미터

- `page` (int, default: 1)
- `per_page` (int, default: 20)
- `status` (string, optional): 상태 필터

### 응답

`GET /api/posts`와 유사하지만 모든 상태의 게시글 조회 가능

## DELETE /api/admin/posts/{id}

게시글 삭제 (관리자)

**인증 필요 (관리자 권한)**

### 응답

**성공 (200)**
```json
{
  "message": "게시글이 삭제되었습니다."
}
```

