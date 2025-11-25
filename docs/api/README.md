# API 명세서

이 디렉토리에는 모든 API 엔드포인트의 상세 명세가 포함되어 있습니다.

## API 기본 정보

- **Base URL**: `http://localhost:8000/api`
- **인증 방식**: JWT Bearer Token
- **Content-Type**: `application/json`

## 인증

대부분의 API는 인증이 필요합니다. 인증이 필요한 경우 요청 헤더에 다음을 포함해야 합니다:

```
Authorization: Bearer <token>
```

## 응답 형식

### 성공 응답
```json
{
  "data": {...},
  "message": "성공 메시지"
}
```

### 에러 응답
```json
{
  "error": "에러 메시지"
}
```

## HTTP 상태 코드

- `200`: 성공
- `201`: 생성 성공
- `400`: 잘못된 요청
- `401`: 인증 필요
- `403`: 권한 없음
- `404`: 리소스를 찾을 수 없음
- `500`: 서버 오류

## API 목록

- [인증 API](./auth.md)
- [게시글 API](./posts.md)
- [댓글 API](./comments.md)
- [신고 API](./reports.md)
- [관리자 API](./admin.md)

