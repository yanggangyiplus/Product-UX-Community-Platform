"""
Product UX Community Platform Backend
소셜 로그인 기반 커뮤니티 플랫폼 백엔드 서버
"""
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def health_check():
    """서버 상태 확인 엔드포인트"""
    return {'status': 'ok', 'message': 'Product UX Community Platform API'}

@app.route('/api/health')
def api_health():
    """API 상태 확인 엔드포인트"""
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(debug=True, port=8000)

