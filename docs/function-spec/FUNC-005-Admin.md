# FUNC-005: 관리자 기능

## 개요
관리자가 커뮤니티를 관리하기 위한 기능들을 제공합니다.

## 기능 목록

### FUNC-005-01: 회원 관리
- **설명**: 회원 목록 조회 및 관리
- **엔드포인트**: `GET /api/admin/users`
- **인증**: 필요 (`@admin_required`)
- **쿼리 파라미터**:
  - `page` (int, default: 1): 페이지 번호
  - `per_page` (int, default: 20): 페이지당 항목 수
  - `search` (string, optional): 검색어 (이메일/닉네임)
- **응답**: `{ users: [...], total: int, page: int, per_page: int }`

### FUNC-005-02: 회원 정보 수정
- **설명**: 회원의 역할 또는 활성화 상태 변경
- **엔드포인트**: `PUT /api/admin/users/<id>`
- **인증**: 필요 (`@admin_required`)
- **요청 본문**:
  - `is_active` (boolean, optional): 활성화 여부
  - `role` (string, optional): 역할 (user/admin)
- **응답**: `{ message: string }`

### FUNC-005-03: 게시글 관리
- **설명**: 모든 게시글 조회 (관리자용)
- **엔드포인트**: `GET /api/admin/posts`
- **인증**: 필요 (`@admin_required`)
- **쿼리 파라미터**:
  - `page` (int, default: 1): 페이지 번호
  - `per_page` (int, default: 20): 페이지당 항목 수
  - `status` (string, optional): 상태 필터
- **응답**: `{ posts: [...], total: int, page: int, per_page: int }`

### FUNC-005-04: 게시글 삭제 (관리자)
- **설명**: 관리자가 게시글 삭제
- **엔드포인트**: `DELETE /api/admin/posts/<id>`
- **인증**: 필요 (`@admin_required`)
- **응답**: `{ message: string }`
- **차이점**: 작성자 권한 없이도 삭제 가능

### FUNC-005-05: 카테고리 관리
- **설명**: 게시판 카테고리 생성, 수정, 삭제
- **데이터 모델**: Category
- **기능**:
  - 카테고리 목록 조회
  - 카테고리 생성
  - 카테고리 수정 (이름, 설명, 순서)
  - 카테고리 활성화/비활성화
  - 카테고리 삭제
- **주의사항**: 게시글이 있는 카테고리 삭제 시 처리 필요

## 권한 관리
- **일반 사용자**: 자신의 게시글/댓글만 수정/삭제 가능
- **관리자**: 모든 게시글/댓글 수정/삭제 가능, 신고 처리 가능, 회원 관리 가능

## 데이터 모델

### Category
- `id`: 카테고리 ID
- `name`: 카테고리 이름
- `description`: 설명
- `order`: 정렬 순서
- `is_active`: 활성화 여부

## 관련 문서
- API 명세: `docs/api/admin.md`

