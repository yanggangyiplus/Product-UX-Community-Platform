"""
테스트 데이터 생성 스크립트
"""
from database import SessionLocal, init_db
from models import User, Post, Category, UserRole, PostStatus
import hashlib
from datetime import datetime

def create_test_data():
    """테스트 데이터 생성"""
    init_db()
    db = SessionLocal()
    
    try:
        # 테스트 사용자 생성
        user = User(
            email="test@example.com",
            password_hash=hashlib.sha256("password123".encode()).hexdigest(),
            nickname="테스트 사용자",
            role=UserRole.USER,
            is_active=True
        )
        db.add(user)
        
        # 관리자 사용자 생성
        admin = User(
            email="admin@example.com",
            password_hash=hashlib.sha256("admin123".encode()).hexdigest(),
            nickname="관리자",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin)
        db.flush()
        
        # 카테고리 생성
        category1 = Category(
            name="일반",
            description="일반 게시글",
            order=1,
            is_active=True
        )
        category2 = Category(
            name="질문",
            description="질문 게시글",
            order=2,
            is_active=True
        )
        db.add(category1)
        db.add(category2)
        db.flush()
        
        # 테스트 게시글 생성
        post1 = Post(
            author_id=user.id,
            category_id=category1.id,
            title="테스트 게시글 1",
            content="이것은 테스트 게시글입니다.",
            status=PostStatus.PUBLISHED,
            view_count=10,
            like_count=5,
            comment_count=2
        )
        post2 = Post(
            author_id=user.id,
            category_id=category2.id,
            title="테스트 게시글 2",
            content="질문 게시글입니다.",
            status=PostStatus.PUBLISHED,
            view_count=20,
            like_count=10,
            comment_count=5
        )
        db.add(post1)
        db.add(post2)
        
        db.commit()
        print("테스트 데이터가 생성되었습니다.")
        print(f"- 일반 사용자: test@example.com / password123")
        print(f"- 관리자: admin@example.com / admin123")
    except Exception as e:
        db.rollback()
        print(f"오류 발생: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()

