"""
인증 관련 유틸리티 함수
JWT 토큰 생성 및 검증
"""
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from models import User, UserRole


def generate_token(user_id, role):
    """JWT 토큰 생성"""
    payload = {
        'user_id': user_id,
        'role': role.value if isinstance(role, UserRole) else role,
        'exp': datetime.utcnow() + timedelta(seconds=int(os.getenv('JWT_EXPIRATION_DELTA', '86400'))),
        'iat': datetime.utcnow()
    }
    secret_key = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    algorithm = os.getenv('JWT_ALGORITHM', 'HS256')
    
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def verify_token(token):
    """JWT 토큰 검증"""
    try:
        secret_key = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
        algorithm = os.getenv('JWT_ALGORITHM', 'HS256')
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def login_required(f):
    """로그인 필요 데코레이터"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': '토큰이 필요합니다.'}), 401
        
        # Bearer 토큰 형식 처리
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': '유효하지 않은 토큰입니다.'}), 401
        
        # request에 사용자 정보 추가
        request.current_user_id = payload['user_id']
        request.current_user_role = payload['role']
        
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """관리자 권한 필요 데코레이터"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if request.current_user_role != UserRole.ADMIN.value:
            return jsonify({'error': '관리자 권한이 필요합니다.'}), 403
        return f(*args, **kwargs)
    return decorated_function

