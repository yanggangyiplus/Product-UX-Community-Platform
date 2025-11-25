# FUNC-002: 게시글 관리

## 개요
게시글 작성, 조회, 수정, 삭제 기능을 제공합니다. 임시저장 기능을 포함합니다.

## 기능 목록

### FUNC-002-01: 게시글 목록 조회
- **설명**: 게시글 목록을 페이지네이션으로 조회
- **엔드포인트**: `GET /api/posts`
- **쿼리 파라미터**:
  - `page` (int, default: 1): 페이지 번호
  - `per_page` (int, default: 20): 페이지당 항목 수
  - `category_id` (int, optional): 카테고리 필터
  - `search` (string, optional): 검색어 (제목/내용)
- **응답**:
  - 성공: `{ posts: [...], total: int, page: int, per_page: int }`
- **정렬**: 생성일시 내림차순

### FUNC-002-02: 게시글 상세 조회
- **설명**: 특정 게시글의 상세 정보 조회
- **엔드포인트**: `GET /api/posts/<id>`
- **파라미터**:
  - `id` (path): 게시글 ID
- **응답**:
  - 성공: 게시글 상세 정보 (제목, 내용, 작성자, 이미지 등)
  - 실패: `{ error: string }`
- **부가 기능**: 조회수 자동 증가

### FUNC-002-03: 게시글 작성
- **설명**: 새 게시글 작성
- **엔드포인트**: `POST /api/posts`
- **인증**: 필요 (`@login_required`)
- **요청 본문**:
  - `title` (string, required): 제목 (최대 500자)
  - `content` (string, required): 내용
  - `category_id` (int, optional): 카테고리 ID
  - `images` (array, optional): 이미지 URL 배열
  - `status` (string, optional): 상태 (published/draft)
- **응답**:
  - 성공: `{ id: int, message: string }`
  - 실패: `{ error: string }`

### FUNC-002-04: 게시글 수정
- **설명**: 기존 게시글 수정
- **엔드포인트**: `PUT /api/posts/<id>`
- **인증**: 필요 (작성자만 수정 가능)
- **요청 본문**: FUNC-002-03과 동일 (모든 필드 optional)
- **권한 확인**: 작성자 ID와 현재 사용자 ID 비교

### FUNC-002-05: 게시글 삭제
- **설명**: 게시글 삭제 (소프트 삭제)
- **엔드포인트**: `DELETE /api/posts/<id>`
- **인증**: 필요 (작성자만 삭제 가능)
- **처리**: `status`를 `DELETED`로 변경
- **응답**: `{ message: string }`

### FUNC-002-06: 게시글 좋아요
- **설명**: 게시글에 좋아요 추가/제거
- **엔드포인트**: `POST /api/posts/<id>/like`
- **인증**: 필요
- **동작**:
  - 이미 좋아요한 경우: 좋아요 취소
  - 좋아요하지 않은 경우: 좋아요 추가
- **응답**: `{ message: string, like_count: int }`
- **제약조건**: 같은 사용자가 같은 게시글에 중복 좋아요 불가

### FUNC-002-07: 임시저장
- **설명**: 게시글을 임시저장 상태로 저장
- **상태**: `status = 'draft'`
- **유효성 검사**: 제목/내용 없어도 가능
- **용도**: 작성 중인 게시글을 나중에 완성하기 위해 저장

## 데이터 모델

### Post
- `id`: 게시글 ID
- `author_id`: 작성자 ID (FK)
- `category_id`: 카테고리 ID (FK, nullable)
- `title`: 제목
- `content`: 내용
- `status`: 상태 (PUBLISHED/DRAFT/DELETED)
- `view_count`: 조회수
- `like_count`: 좋아요 수
- `comment_count`: 댓글 수

### PostImage
- `id`: 이미지 ID
- `post_id`: 게시글 ID (FK)
- `image_url`: 이미지 URL
- `order`: 순서

### PostLike
- `id`: 좋아요 ID
- `user_id`: 사용자 ID (FK)
- `post_id`: 게시글 ID (FK)
- **제약조건**: (user_id, post_id) 유니크

## 관련 문서
- UX Flow: `docs/UX-flow/02-Post-Write-Flow.md`
- API 명세: `docs/api/posts.md`

