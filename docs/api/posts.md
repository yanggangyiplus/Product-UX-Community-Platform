# 게시글 API

## GET /api/posts

게시글 목록 조회

### 쿼리 파라미터

- `page` (int, default: 1): 페이지 번호
- `per_page` (int, default: 20): 페이지당 항목 수
- `category_id` (int, optional): 카테고리 필터
- `search` (string, optional): 검색어

### 요청 예시

```http
GET /api/posts?page=1&per_page=20&category_id=1&search=제목
```

### 응답

**성공 (200)**
```json
{
  "posts": [
    {
      "id": 1,
      "title": "게시글 제목",
      "content": "게시글 내용 미리보기...",
      "author_id": 1,
      "author_nickname": "작성자",
      "category_id": 1,
      "category_name": "카테고리",
      "view_count": 100,
      "like_count": 10,
      "comment_count": 5,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 100,
  "page": 1,
  "per_page": 20
}
```

## GET /api/posts/{id}

게시글 상세 조회

### 경로 파라미터

- `id` (int, required): 게시글 ID

### 응답

**성공 (200)**
```json
{
  "id": 1,
  "title": "게시글 제목",
  "content": "게시글 전체 내용",
  "author_id": 1,
  "author_nickname": "작성자",
  "category_id": 1,
  "category_name": "카테고리",
  "view_count": 101,
  "like_count": 10,
  "comment_count": 5,
  "images": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg"
  ],
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

## POST /api/posts

게시글 작성

**인증 필요**

### 요청 본문

```json
{
  "title": "게시글 제목",
  "content": "게시글 내용",
  "category_id": 1,
  "images": ["https://example.com/image.jpg"],
  "status": "published"
}
```

### 응답

**성공 (201)**
```json
{
  "id": 1,
  "message": "게시글이 작성되었습니다."
}
```

## PUT /api/posts/{id}

게시글 수정

**인증 필요 (작성자만)**

### 요청 본문

```json
{
  "title": "수정된 제목",
  "content": "수정된 내용",
  "category_id": 2,
  "status": "published"
}
```

### 응답

**성공 (200)**
```json
{
  "message": "게시글이 수정되었습니다."
}
```

## DELETE /api/posts/{id}

게시글 삭제

**인증 필요 (작성자만)**

### 응답

**성공 (200)**
```json
{
  "message": "게시글이 삭제되었습니다."
}
```

## POST /api/posts/{id}/like

게시글 좋아요

**인증 필요**

### 응답

**성공 (200)**
```json
{
  "message": "좋아요가 추가되었습니다.",
  "like_count": 11
}
```

