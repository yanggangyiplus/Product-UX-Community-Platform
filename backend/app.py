"""
Product UX Community Platform Backend
소셜 로그인 기반 커뮤니티 플랫폼 백엔드 서버
"""
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)

# CORS 설정 (환경 변수에서 허용된 오리진 가져오기)
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
CORS(app, origins=cors_origins)

# 환경 변수에서 설정값 가져오기
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
app.config['PORT'] = int(os.getenv('FLASK_PORT', '8000'))

# 데이터베이스 설정
app.config['DB_HOST'] = os.getenv('DB_HOST', 'localhost')
app.config['DB_PORT'] = int(os.getenv('DB_PORT', '3306'))
app.config['DB_USER'] = os.getenv('DB_USER', 'root')
app.config['DB_PASSWORD'] = os.getenv('DB_PASSWORD', '')
app.config['DB_NAME'] = os.getenv('DB_NAME', 'community_platform')

# JWT 설정
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_ALGORITHM'] = os.getenv('JWT_ALGORITHM', 'HS256')
app.config['JWT_EXPIRATION_DELTA'] = int(os.getenv('JWT_EXPIRATION_DELTA', '86400'))

# OAuth 설정
app.config['KAKAO_CLIENT_ID'] = os.getenv('KAKAO_CLIENT_ID', '')
app.config['KAKAO_CLIENT_SECRET'] = os.getenv('KAKAO_CLIENT_SECRET', '')
app.config['KAKAO_REDIRECT_URI'] = os.getenv('KAKAO_REDIRECT_URI', '')

app.config['NAVER_CLIENT_ID'] = os.getenv('NAVER_CLIENT_ID', '')
app.config['NAVER_CLIENT_SECRET'] = os.getenv('NAVER_CLIENT_SECRET', '')
app.config['NAVER_REDIRECT_URI'] = os.getenv('NAVER_REDIRECT_URI', '')

app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID', '')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET', '')
app.config['GOOGLE_REDIRECT_URI'] = os.getenv('GOOGLE_REDIRECT_URI', '')

# 라우트 등록
from routes.auth import auth_bp
from routes.posts import posts_bp
from routes.comments import comments_bp
from routes.reports import reports_bp
from routes.admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(comments_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def health_check():
    """서버 상태 확인 엔드포인트"""
    return {'status': 'ok', 'message': 'Product UX Community Platform API'}

@app.route('/api/health')
def api_health():
    """API 상태 확인 엔드포인트"""
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])

