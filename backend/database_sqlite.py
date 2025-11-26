"""
데이터베이스 연결 및 초기화 모듈 (SQLite 버전)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base

# SQLite 사용 (파일 기반)
engine = create_engine(
    'sqlite:///community_platform.db',
    pool_pre_ping=True,
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
