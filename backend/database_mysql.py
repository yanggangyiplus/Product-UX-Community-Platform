"""
데이터베이스 연결 및 초기화 모듈 (SQLite)
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base

# SQLite 사용 (파일 기반 - MySQL 없이 작동)
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'community_platform.db')
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

# 데이터베이스 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False},  # SQLite용 설정
    echo=False
)

# 세션 팩토리 생성
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    """데이터베이스 테이블 생성"""
    Base.metadata.create_all(bind=engine)
    print("데이터베이스 테이블이 생성되었습니다.")

def get_db():
    """데이터베이스 세션 생성 (의존성 주입용)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
