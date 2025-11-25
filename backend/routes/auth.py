"""
인증 관련 API 라우트
/login, /callback 엔드포인트 포함
"""
from flask import Blueprint, request, jsonify, redirect
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, OAuthAccount, OAuthProvider, UserRole
from utils.auth import generate_token
from utils.oauth import (
    get_kakao_auth_url, get_naver_auth_url, get_google_auth_url,
    get_kakao_token, get_naver_token, get_google_token,
    get_kakao_user_info, get_naver_user_info, get_google_user_info
)
import hashlib
import secrets

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """일반 로그인 (이메일/비밀번호)"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': '이메일과 비밀번호를 입력해주세요.'}), 400
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not user.password_hash:
            return jsonify({'error': '이메일 또는 비밀번호가 올바르지 않습니다.'}), 401
        
        # 비밀번호 검증 (실제 구현 시 bcrypt 등 사용)
        # 여기서는 간단히 해시 비교
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user.password_hash != password_hash:
            return jsonify({'error': '이메일 또는 비밀번호가 올바르지 않습니다.'}), 401
        
        if not user.is_active:
            return jsonify({'error': '비활성화된 계정입니다.'}), 403
        
        token = generate_token(user.id, user.role)
        
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'nickname': user.nickname,
                'role': user.role.value
            }
        }), 200
    finally:
        db.close()


@auth_bp.route('/oauth/<provider>', methods=['GET'])
def oauth_login(provider):
    """OAuth 로그인 시작 (리다이렉트 URL 반환)"""
    provider = provider.lower()
    
    if provider == 'kakao':
        auth_url = get_kakao_auth_url()
    elif provider == 'naver':
        state = secrets.token_urlsafe(32)
        auth_url = get_naver_auth_url(state)
    elif provider == 'google':
        state = secrets.token_urlsafe(32)
        auth_url = get_google_auth_url(state)
    else:
        return jsonify({'error': '지원하지 않는 OAuth 제공자입니다.'}), 400
    
    return jsonify({'auth_url': auth_url}), 200


@auth_bp.route('/callback/<provider>', methods=['GET'])
def oauth_callback(provider):
    """OAuth 콜백 처리"""
    provider = provider.lower()
    code = request.args.get('code')
    state = request.args.get('state')
    
    if not code:
        return jsonify({'error': '인증 코드가 없습니다.'}), 400
    
    db = SessionLocal()
    try:
        # 토큰 교환
        if provider == 'kakao':
            token_data = get_kakao_token(code)
            if not token_data:
                return jsonify({'error': '카카오 인증에 실패했습니다.'}), 400
            access_token = token_data.get('access_token')
            user_info = get_kakao_user_info(access_token)
            provider_user_id = str(user_info.get('id'))
            nickname = user_info.get('kakao_account', {}).get('profile', {}).get('nickname', '')
            email = user_info.get('kakao_account', {}).get('email', '')
            
        elif provider == 'naver':
            token_data = get_naver_token(code, state)
            if not token_data:
                return jsonify({'error': '네이버 인증에 실패했습니다.'}), 400
            access_token = token_data.get('access_token')
            user_info = get_naver_user_info(access_token)
            provider_user_id = user_info.get('response', {}).get('id')
            nickname = user_info.get('response', {}).get('nickname', '')
            email = user_info.get('response', {}).get('email', '')
            
        elif provider == 'google':
            token_data = get_google_token(code)
            if not token_data:
                return jsonify({'error': '구글 인증에 실패했습니다.'}), 400
            access_token = token_data.get('access_token')
            user_info = get_google_user_info(access_token)
            provider_user_id = user_info.get('id')
            nickname = user_info.get('name', '')
            email = user_info.get('email', '')
            
        else:
            return jsonify({'error': '지원하지 않는 OAuth 제공자입니다.'}), 400
        
        # OAuth 계정 찾기 또는 생성
        oauth_provider = OAuthProvider[provider.upper()]
        oauth_account = db.query(OAuthAccount).filter(
            OAuthAccount.provider == oauth_provider,
            OAuthAccount.provider_user_id == provider_user_id
        ).first()
        
        if oauth_account:
            user = oauth_account.user
            # 토큰 업데이트
            oauth_account.access_token = access_token
            oauth_account.refresh_token = token_data.get('refresh_token')
        else:
            # 새 사용자 생성
            user = User(
                email=email if email else None,
                nickname=nickname or f'{provider}_user_{provider_user_id[:8]}',
                role=UserRole.USER
            )
            db.add(user)
            db.flush()
            
            oauth_account = OAuthAccount(
                user_id=user.id,
                provider=oauth_provider,
                provider_user_id=provider_user_id,
                access_token=access_token,
                refresh_token=token_data.get('refresh_token')
            )
            db.add(oauth_account)
        
        db.commit()
        
        token = generate_token(user.id, user.role)
        
        # 프론트엔드로 리다이렉트 (토큰 포함)
        frontend_url = f"http://localhost:3000/auth/callback?token={token}&provider={provider}"
        return redirect(frontend_url)
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'OAuth 처리 중 오류가 발생했습니다: {str(e)}'}), 500
    finally:
        db.close()

