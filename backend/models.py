"""
데이터베이스 모델 정의
User, Post, Comment, Report, Admin, OAuthAccount 모델 포함
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class UserRole(enum.Enum):
    """사용자 역할"""
    USER = "user"
    ADMIN = "admin"


class OAuthProvider(enum.Enum):
    """OAuth 제공자"""
    KAKAO = "kakao"
    NAVER = "naver"
    GOOGLE = "google"


class PostStatus(enum.Enum):
    """게시글 상태"""
    PUBLISHED = "published"
    DRAFT = "draft"
    DELETED = "deleted"


class ReportStatus(enum.Enum):
    """신고 상태"""
    PENDING = "pending"
    PROCESSING = "processing"
    RESOLVED = "resolved"
    REJECTED = "rejected"


class ReportType(enum.Enum):
    """신고 유형"""
    POST = "post"
    COMMENT = "comment"


class User(Base):
    """사용자 모델"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=True)  # 일반 로그인용
    nickname = Column(String(100), nullable=False)
    profile_image_url = Column(String(500), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 관계
    oauth_accounts = relationship("OAuthAccount", back_populates="user", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    reports = relationship("Report", foreign_keys="Report.reporter_id", back_populates="reporter", cascade="all, delete-orphan")
    likes = relationship("PostLike", foreign_keys="PostLike.user_id", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, nickname={self.nickname})>"


class OAuthAccount(Base):
    """OAuth 계정 모델 (소셜 로그인 연동 정보)"""
    __tablename__ = 'oauth_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    provider = Column(Enum(OAuthProvider), nullable=False)
    provider_user_id = Column(String(255), nullable=False)  # OAuth 제공자의 사용자 ID
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 관계
    user = relationship("User", back_populates="oauth_accounts")

    # 복합 유니크 제약조건: 같은 제공자에서 같은 사용자 ID는 하나만
    __table_args__ = (
        {'mysql_engine': 'InnoDB'},
    )

    def __repr__(self):
        return f"<OAuthAccount(id={self.id}, provider={self.provider.value}, user_id={self.user_id})>"


class Category(Base):
    """게시판 카테고리 모델"""
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    order = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 관계
    posts = relationship("Post", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"


class Post(Base):
    """게시글 모델"""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Enum(PostStatus), default=PostStatus.PUBLISHED, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    like_count = Column(Integer, default=0, nullable=False)
    comment_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 관계
    author = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("PostLike", back_populates="post", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="post", cascade="all, delete-orphan")
    images = relationship("PostImage", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title[:50]}, author_id={self.author_id})>"


class PostImage(Base):
    """게시글 이미지 모델"""
    __tablename__ = 'post_images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    image_url = Column(String(500), nullable=False)
    order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 관계
    post = relationship("Post", back_populates="images")

    def __repr__(self):
        return f"<PostImage(id={self.id}, post_id={self.post_id})>"


class PostLike(Base):
    """게시글 좋아요 모델"""
    __tablename__ = 'post_likes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 관계
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

    # 복합 유니크 제약조건: 같은 사용자가 같은 게시글에 중복 좋아요 불가
    __table_args__ = (
        {'mysql_engine': 'InnoDB'},
    )

    def __repr__(self):
        return f"<PostLike(id={self.id}, user_id={self.user_id}, post_id={self.post_id})>"


class Comment(Base):
    """댓글 모델"""
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    parent_id = Column(Integer, ForeignKey('comments.id', ondelete='CASCADE'), nullable=True)  # 대댓글용
    content = Column(Text, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 관계
    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")
    reports = relationship("Report", back_populates="comment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Comment(id={self.id}, post_id={self.post_id}, author_id={self.author_id})>"


class Report(Base):
    """신고 모델"""
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reporter_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    report_type = Column(Enum(ReportType), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=True)
    comment_id = Column(Integer, ForeignKey('comments.id', ondelete='CASCADE'), nullable=True)
    reason = Column(Text, nullable=False)
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING, nullable=False)
    admin_note = Column(Text, nullable=True)
    processed_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    processed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 관계
    reporter = relationship("User", foreign_keys=[reporter_id], back_populates="reports")
    post = relationship("Post", back_populates="reports")
    comment = relationship("Comment", back_populates="reports")
    processor = relationship("User", foreign_keys=[processed_by])

    def __repr__(self):
        return f"<Report(id={self.id}, report_type={self.report_type.value}, status={self.status.value})>"

