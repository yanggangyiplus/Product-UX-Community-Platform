"""
로깅 설정 유틸리티
애플리케이션 전체 로깅 관리
"""
import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(app):
    """Flask 앱에 로깅 설정"""

    # 로그 디렉토리 생성
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 로그 레벨 설정
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    app.logger.setLevel(getattr(logging, log_level))

    # 파일 핸들러 설정 (로테이션)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)

    # 에러 로그 파일 핸들러
    error_file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'error.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    error_file_handler.setLevel(logging.ERROR)

    # 로그 포맷 설정
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    error_file_handler.setFormatter(formatter)

    # 핸들러 추가
    app.logger.addHandler(file_handler)
    app.logger.addHandler(error_file_handler)

    # 콘솔 핸들러 (개발 환경용)
    if app.config.get('DEBUG'):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)

    app.logger.info('로깅 시스템이 초기화되었습니다')
