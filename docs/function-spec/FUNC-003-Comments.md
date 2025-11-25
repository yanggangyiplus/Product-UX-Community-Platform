# FUNC-003: 댓글 관리

## 개요
게시글에 대한 댓글 작성, 조회, 수정, 삭제 기능을 제공합니다. 대댓글 기능을 포함합니다.

## 기능 목록

### FUNC-003-01: 댓글 목록 조회
- **설명**: 특정 게시글의 댓글 목록 조회 (트리 구조)
- **엔드포인트**: `GET /api/comments`
- **쿼리 파라미터**:
  - `post_id` (int, required): 게시글 ID
- **응답**:
  - 성공: `{ comments: [...] }` (트리 구조)
  - 댓글은 부모-자식 관계로 구성됨
- **정렬**: 생성일시 오름차순

### FUNC-003-02: 댓글 작성
- **설명**: 새 댓글 작성
- **엔드포인트**: `POST /api/comments`
- **인증**: 필요 (`@login_required`)
- **요청 본문**:
  - `post_id` (int, required): 게시글 ID
  - `content` (string, required): 댓글 내용
  - `parent_id` (int, optional): 부모 댓글 ID (대댓글용)
- **응답**:
  - 성공: `{ id: int, message: string }`
  - 실패: `{ error: string }`
- **부가 기능**: 게시글의 `comment_count` 자동 증가

### FUNC-003-03: 댓글 수정
- **설명**: 기존 댓글 수정
- **엔드포인트**: `PUT /api/comments/<id>`
- **인증**: 필요 (작성자만 수정 가능)
- **요청 본문**:
  - `content` (string, required): 수정할 내용
- **권한 확인**: 작성자 ID와 현재 사용자 ID 비교

### FUNC-003-04: 댓글 삭제
- **설명**: 댓글 삭제 (소프트 삭제)
- **엔드포인트**: `DELETE /api/comments/<id>`
- **인증**: 필요 (작성자만 삭제 가능)
- **처리**: `is_deleted = true`로 설정
- **부가 기능**: 게시글의 `comment_count` 자동 감소

## 데이터 모델

### Comment
- `id`: 댓글 ID
- `post_id`: 게시글 ID (FK)
- `author_id`: 작성자 ID (FK)
- `parent_id`: 부모 댓글 ID (FK, nullable, 대댓글용)
- `content`: 댓글 내용
- `is_deleted`: 삭제 여부

## 대댓글 구조
- `parent_id`가 `null`이면 최상위 댓글
- `parent_id`가 있으면 해당 댓글의 대댓글
- 무한 깊이 지원 가능 (실제로는 제한 권장)

## 관련 문서
- API 명세: `docs/api/comments.md`

