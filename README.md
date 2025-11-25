# Product UX Community Platform

소셜 로그인 기반 커뮤니티 플랫폼 - 기획·UX 설계·사용자 행동 기반 개선 프로젝트

## 프로젝트 소개

이 프로젝트는 신규 서비스 기획, UX 설계, 사용자 행동 기반 UX 개선까지 하나의 프로젝트에 통합한 End-to-End 기획·UX 포트폴리오 프로젝트입니다.

### 주요 특징

- **신규 서비스 기획**: 소셜 로그인 기반 커뮤니티 플랫폼 전체 구조 설계 (요구사항 → 기능명세 → IA → UX → UI)
- **UX 설계**: 핵심 사용자 플로우 정의, 예외 처리 설계, Figma 와이어프레임 제작
- **UX 개선**: 사용자 행동 분석 기반 Pain Point 도출 및 개선안 제시

## 프로젝트 목적

- 접근성 높은 커뮤니티 경험 제공
- 직관적인 탐색 UX 설계
- 운영자(Admin) 관리 비용 최소화
- 사용자 행동 기반 개선안까지 포함해 PO/기획/UX 역량을 완성형으로 표현

## 주요 기능

### 인증 시스템
- 소셜 로그인 (OAuth 2.0): 카카오/네이버/구글 인증
- 일반 로그인: 이메일 + 비밀번호 기반
- 비밀번호 재설정 기능

### 커뮤니티 기능
- 게시판: 카테고리 기반 검색·정렬
- 게시글 CRUD: 이미지 업로드·임시저장 포함
- 댓글/대댓글: 기본 커뮤니티 기능
- 좋아요: 반응 기반 랭킹
- 신고 기능: 게시글·댓글 신고 및 중복방지

### 관리자 기능
- 신고 처리
- 회원 관리
- 게시판 관리

## 기술 스택

### Frontend
- React 18.2
- React Router DOM
- Vite
- Axios

### Backend
- Python 3.x
- Flask
- SQLAlchemy
- OAuth2.0 인증 구조

### Database
- MySQL 또는 PostgreSQL

## 📁 프로젝트 구조

```
Product-UX-Community-Platform/
├── frontend/                 # React 프론트엔드
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── backend/                  # Flask 백엔드
│   ├── app.py
│   └── requirements.txt
├── docs/                     # 프로젝트 문서
│   ├── requirements/         # 요구사항정의서 (REQ-001 ~)
│   ├── function-spec/        # 기능명세(FUNC-001 ~)
│   ├── UX-research/          # Pain Point 분석 + 개선안
│   ├── IA/                   # 정보구조도
│   ├── UX-flow/              # 유저 플로우 다이어그램
│   └── wireframes/           # Figma 와이어프레임
└── README.md
```

## 시작하기

### 사전 요구사항

- Node.js 18.x 이상
- Python 3.9 이상
- MySQL 또는 PostgreSQL

### 설치 및 실행

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

프론트엔드는 `http://localhost:3000`에서 실행됩니다.

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

백엔드는 `http://localhost:8000`에서 실행됩니다.

### 환경 변수 설정

백엔드 환경 변수는 `backend/.env.example` 파일을 참조하여 `.env` 파일을 생성하세요.

## 정보구조(IA)

```
Home
├─ 로그인
│   ├─ 소셜 로그인 (카카오/네이버/구글)
│   ├─ 일반 로그인
│   └─ PW 재설정
├─ 게시판
│   ├─ 카테고리 목록
│   ├─ 게시글 목록
│   └─ 상세보기
│       ├─ 댓글/대댓글
│       └─ 신고
├─ 글쓰기
│   ├─ 작성
│   └─ 임시저장
├─ 마이페이지
│   ├─ 내 글
│   ├─ 내 댓글
│   └─ 프로필 수정
└─ 관리자 페이지
    ├─ 신고관리
    ├─ 회원관리
    └─ 게시판관리
```

## 산출물

- 요구사항정의서 (REQ 문서)
- 기능명세서 (FUNC)
- IA 다이어그램
- UX Flow
- Figma Wireframe
- UX 문제 분석 보고서
- 개선안 제안서 (Before → After)
- 개선된 프로토타입(Figma)

## 이 프로젝트가 보여주는 역량

| 역량 영역 | 내용 |
|---------|------|
| 기획 역량 | 신규 서비스 전체 기획, IA/Flow 구조 설계 |
| UX 디자인 | UX 흐름·와이어프레임·예외처리 설계 |
| 사용자 분석 | 행동 기반 Pain Point 도출 & 개선 능력 |
| PO 역량 | 신규 기획 + 개선 + 운영 관점 통합 |
| 개발 이해도 | OAuth / API Flow / DB 기반 이해 |

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 작성자

HANGAYEONG

## 최종 목표

단순한 기능 구현 중심 프로젝트가 아니라 **"사용자 경험 기반으로 기획·UX·개선까지 완성한 제품 수준의 프로젝트"**를 만드는 것을 목표로 합니다.
