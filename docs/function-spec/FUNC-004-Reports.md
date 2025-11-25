# FUNC-004: 신고 시스템

## 개요
부적절한 게시글 또는 댓글을 신고하는 기능과 관리자의 신고 처리 기능을 제공합니다.

## 기능 목록

### FUNC-004-01: 신고 생성
- **설명**: 게시글 또는 댓글 신고
- **엔드포인트**: `POST /api/reports`
- **인증**: 필요 (`@login_required`)
- **요청 본문**:
  - `report_type` (string, required): 신고 유형 (post/comment)
  - `post_id` (int, conditional): 게시글 ID (report_type이 post일 때)
  - `comment_id` (int, conditional): 댓글 ID (report_type이 comment일 때)
  - `reason` (string, required): 신고 사유
- **응답**:
  - 성공: `{ id: int, message: string }`
  - 실패: `{ error: string }`
- **중복 방지**: 같은 사용자가 같은 항목을 이미 신고한 경우 에러 반환

### FUNC-004-02: 신고 목록 조회 (관리자)
- **설명**: 관리자가 신고 목록 조회
- **엔드포인트**: `GET /api/admin/reports`
- **인증**: 필요 (`@admin_required`)
- **쿼리 파라미터**:
  - `status` (string, optional): 상태 필터 (pending/processing/resolved/rejected)
  - `page` (int, default: 1): 페이지 번호
  - `per_page` (int, default: 20): 페이지당 항목 수
- **응답**: `{ reports: [...], total: int, page: int, per_page: int }`

### FUNC-004-03: 신고 상태 변경 (관리자)
- **설명**: 관리자가 신고 상태 변경
- **엔드포인트**: `PUT /api/admin/reports/<id>`
- **인증**: 필요 (`@admin_required`)
- **요청 본문**:
  - `status` (string, required): 새 상태 (pending/processing/resolved/rejected)
  - `admin_note` (string, optional): 처리 사유
- **응답**: `{ message: string }`
- **부가 기능**: `processed_by`, `processed_at` 자동 기록

## 데이터 모델

### Report
- `id`: 신고 ID
- `reporter_id`: 신고자 ID (FK)
- `report_type`: 신고 유형 (POST/COMMENT)
- `post_id`: 게시글 ID (FK, nullable)
- `comment_id`: 댓글 ID (FK, nullable)
- `reason`: 신고 사유
- `status`: 상태 (PENDING/PROCESSING/RESOLVED/REJECTED)
- `admin_note`: 관리자 처리 사유
- `processed_by`: 처리한 관리자 ID (FK, nullable)
- `processed_at`: 처리 일시 (nullable)

## 신고 상태 흐름
1. **PENDING**: 신고 접수됨 (초기 상태)
2. **PROCESSING**: 관리자가 검토 중
3. **RESOLVED**: 신고가 받아들여져 조치 완료
4. **REJECTED**: 신고가 기각됨

## 중복 신고 방지
- 같은 사용자가 같은 항목에 대해 `PENDING` 상태의 신고가 있으면 중복 신고 불가
- 이미 처리된 신고는 다시 신고 가능 (다른 사유로)

## 관련 문서
- UX Flow: `docs/UX-flow/03-Report-Flow.md`
- API 명세: `docs/api/reports.md`

