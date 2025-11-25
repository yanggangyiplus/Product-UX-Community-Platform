# FUNC-001: 인증 시스템

## 개요
사용자 인증 및 로그인 기능을 제공합니다. 일반 로그인(이메일/비밀번호)과 소셜 로그인(OAuth 2.0)을 지원합니다.

## 기능 목록

### FUNC-001-01: 일반 로그인
- **설명**: 이메일과 비밀번호를 사용한 로그인
- **엔드포인트**: `POST /api/auth/login`
- **요청 파라미터**:
  - `email` (string, required): 사용자 이메일
  - `password` (string, required): 비밀번호
- **응답**:
  - 성공: `{ token: string, user: { id, email, nickname, role } }`
  - 실패: `{ error: string }`
- **에러 처리**:
  - 이메일/비밀번호 불일치: 401
  - 비활성화된 계정: 403
  - 필수 파라미터 누락: 400

### FUNC-001-02: 소셜 로그인 시작
- **설명**: OAuth 제공자(카카오/네이버/구글) 인증 URL 요청
- **엔드포인트**: `GET /api/auth/oauth/<provider>`
- **파라미터**:
  - `provider` (path): kakao, naver, google 중 하나
- **응답**:
  - 성공: `{ auth_url: string }`
  - 실패: `{ error: string }`

### FUNC-001-03: 소셜 로그인 콜백
- **설명**: OAuth 제공자로부터 인증 코드를 받아 토큰으로 교환
- **엔드포인트**: `GET /api/auth/callback/<provider>`
- **파라미터**:
  - `provider` (path): kakao, naver, google 중 하나
  - `code` (query): OAuth 인증 코드
  - `state` (query, optional): 상태값 (네이버/구글)
- **응답**:
  - 성공: 프론트엔드로 리다이렉트 (토큰 포함)
  - 실패: 로그인 페이지로 리다이렉트 (에러 포함)

### FUNC-001-04: JWT 토큰 생성
- **설명**: 사용자 인증 후 JWT 토큰 생성
- **토큰 내용**:
  - `user_id`: 사용자 ID
  - `role`: 사용자 역할 (user/admin)
  - `exp`: 만료 시간
  - `iat`: 발급 시간
- **만료 시간**: 환경 변수 `JWT_EXPIRATION_DELTA` (기본 24시간)

### FUNC-001-05: 토큰 검증
- **설명**: API 요청 시 JWT 토큰 검증
- **데코레이터**: `@login_required`
- **에러 처리**:
  - 토큰 없음: 401
  - 토큰 만료: 401
  - 유효하지 않은 토큰: 401

## 데이터 모델

### User
- `id`: 사용자 ID
- `email`: 이메일 (nullable, 소셜 로그인 사용자는 없을 수 있음)
- `password_hash`: 비밀번호 해시 (일반 로그인용)
- `nickname`: 닉네임
- `role`: 역할 (USER/ADMIN)
- `is_active`: 활성화 여부

### OAuthAccount
- `id`: OAuth 계정 ID
- `user_id`: 사용자 ID (FK)
- `provider`: 제공자 (KAKAO/NAVER/GOOGLE)
- `provider_user_id`: 제공자의 사용자 ID
- `access_token`: 액세스 토큰
- `refresh_token`: 리프레시 토큰

## 보안 고려사항
1. 비밀번호는 해시화하여 저장 (SHA-256, 프로덕션에서는 bcrypt 권장)
2. JWT 시크릿 키는 환경 변수로 관리
3. 토큰은 HTTP-only 쿠키 또는 localStorage에 저장
4. HTTPS 사용 권장

## 관련 문서
- UX Flow: `docs/UX-flow/01-User-Login-Flow.md`
- API 명세: `docs/api/auth.md`

