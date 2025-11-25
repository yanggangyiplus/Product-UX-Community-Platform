# 댓글 API

## GET /api/comments

댓글 목록 조회

### 쿼리 파라미터

- `post_id` (int, required): 게시글 ID

### 요청 예시

```http
GET /api/comments?post_id=1
```

### 응답

**성공 (200)**
```json
{
  "comments": [
    {
      "id": 1,
      "post_id": 1,
      "author_id": 1,
      "author_nickname": "작성자",
      "parent_id": null,
      "content": "댓글 내용",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "replies": [
        {
          "id": 2,
          "post_id": 1,
          "author_id": 2,
          "author_nickname": "댓글 작성자",
          "parent_id": 1,
          "content": "대댓글 내용",
          "created_at": "2024-01-01T01:00:00",
          "updated_at": "2024-01-01T01:00:00",
          "replies": []
        }
      ]
    }
  ]
}
```

## POST /api/comments

댓글 작성

**인증 필요**

### 요청 본문

```json
{
  "post_id": 1,
  "content": "댓글 내용",
  "parent_id": null
}
```

### 응답

**성공 (201)**
```json
{
  "id": 1,
  "message": "댓글이 작성되었습니다."
}
```

## PUT /api/comments/{id}

댓글 수정

**인증 필요 (작성자만)**

### 요청 본문

```json
{
  "content": "수정된 댓글 내용"
}
```

### 응답

**성공 (200)**
```json
{
  "message": "댓글이 수정되었습니다."
}
```

## DELETE /api/comments/{id}

댓글 삭제

**인증 필요 (작성자만)**

### 응답

**성공 (200)**
```json
{
  "message": "댓글이 삭제되었습니다."
}
```

