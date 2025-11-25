# ERD (Entity Relationship Diagram)

## 데이터베이스 모델 구조

### 주요 엔티티

#### 1. User (사용자)
- **기본 정보**: id, email, password_hash, nickname, profile_image_url
- **권한**: role (USER/ADMIN), is_active
- **타임스탬프**: created_at, updated_at
- **관계**: 
  - OAuthAccount (1:N)
  - Post (1:N)
  - Comment (1:N)
  - Report (1:N)
  - PostLike (1:N)

#### 2. OAuthAccount (소셜 로그인 계정)
- **기본 정보**: id, user_id, provider (KAKAO/NAVER/GOOGLE)
- **OAuth 정보**: provider_user_id, access_token, refresh_token
- **관계**: User (N:1)

#### 3. Category (카테고리)
- **기본 정보**: id, name, description, order, is_active
- **관계**: Post (1:N)

#### 4. Post (게시글)
- **기본 정보**: id, author_id, category_id, title, content
- **상태**: status (PUBLISHED/DRAFT/DELETED)
- **통계**: view_count, like_count, comment_count
- **관계**: 
  - User (N:1)
  - Category (N:1)
  - Comment (1:N)
  - PostLike (1:N)
  - PostImage (1:N)
  - Report (1:N)

#### 5. PostImage (게시글 이미지)
- **기본 정보**: id, post_id, image_url, order
- **관계**: Post (N:1)

#### 6. PostLike (게시글 좋아요)
- **기본 정보**: id, user_id, post_id
- **제약조건**: (user_id, post_id) 유니크
- **관계**: User (N:1), Post (N:1)

#### 7. Comment (댓글)
- **기본 정보**: id, post_id, author_id, parent_id, content
- **상태**: is_deleted
- **관계**: 
  - Post (N:1)
  - User (N:1)
  - Comment (self-reference, 대댓글)
  - Report (1:N)

#### 8. Report (신고)
- **기본 정보**: id, reporter_id, report_type (POST/COMMENT)
- **신고 대상**: post_id, comment_id (둘 중 하나)
- **상태**: status (PENDING/PROCESSING/RESOLVED/REJECTED)
- **처리 정보**: admin_note, processed_by, processed_at
- **관계**: 
  - User (reporter) (N:1)
  - User (processor) (N:1)
  - Post (N:1)
  - Comment (N:1)

## 관계 다이어그램

```
User
├── OAuthAccount (1:N)
├── Post (1:N)
├── Comment (1:N)
├── Report (1:N, reporter)
├── Report (1:N, processor)
└── PostLike (1:N)

Category
└── Post (1:N)

Post
├── User (N:1, author)
├── Category (N:1)
├── Comment (1:N)
├── PostLike (1:N)
├── PostImage (1:N)
└── Report (1:N)

Comment
├── Post (N:1)
├── User (N:1, author)
├── Comment (self-reference, parent)
└── Report (1:N)
```

## 주요 제약조건

1. **OAuthAccount**: (provider, provider_user_id) 유니크
2. **PostLike**: (user_id, post_id) 유니크
3. **Report**: post_id와 comment_id 중 하나는 반드시 존재해야 함
4. **User.email**: 유니크 (nullable 허용, 소셜 로그인 사용자는 email 없을 수 있음)

## 인덱스

- User.email (유니크 인덱스)
- Post.author_id
- Post.category_id
- Comment.post_id
- Comment.parent_id
- Report.reporter_id
- Report.status

