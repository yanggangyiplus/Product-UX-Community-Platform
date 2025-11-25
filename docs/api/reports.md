# 신고 API

## POST /api/reports

신고 생성

**인증 필요**

### 요청 본문

```json
{
  "report_type": "post",
  "post_id": 1,
  "reason": "부적절한 내용"
}
```

또는

```json
{
  "report_type": "comment",
  "comment_id": 1,
  "reason": "욕설 사용"
}
```

### 응답

**성공 (201)**
```json
{
  "id": 1,
  "message": "신고가 접수되었습니다."
}
```

**실패 (400) - 중복 신고**
```json
{
  "error": "이미 신고한 항목입니다."
}
```

## GET /api/reports

신고 목록 조회 (관리자용)

**인증 필요 (관리자 권한)**

### 쿼리 파라미터

- `status` (string, optional): 상태 필터 (pending/processing/resolved/rejected)
- `page` (int, default: 1): 페이지 번호
- `per_page` (int, default: 20): 페이지당 항목 수

### 응답

**성공 (200)**
```json
{
  "reports": [
    {
      "id": 1,
      "report_type": "post",
      "post_id": 1,
      "comment_id": null,
      "reason": "부적절한 내용",
      "status": "pending",
      "reporter_id": 2,
      "reporter_nickname": "신고자",
      "admin_note": null,
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 10,
  "page": 1,
  "per_page": 20
}
```

