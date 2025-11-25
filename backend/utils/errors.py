"""
에러 핸들링 유틸리티
표준화된 에러 응답 및 에러 핸들러
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException


class APIError(Exception):
    """사용자 정의 API 에러"""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        rv['status_code'] = self.status_code
        return rv


class ValidationError(APIError):
    """입력 검증 에러"""
    def __init__(self, message, errors=None):
        super().__init__(message, status_code=400, payload={'errors': errors})


class AuthenticationError(APIError):
    """인증 에러"""
    def __init__(self, message="인증이 필요합니다"):
        super().__init__(message, status_code=401)


class AuthorizationError(APIError):
    """권한 에러"""
    def __init__(self, message="권한이 없습니다"):
        super().__init__(message, status_code=403)


class NotFoundError(APIError):
    """리소스를 찾을 수 없음"""
    def __init__(self, message="요청한 리소스를 찾을 수 없습니다"):
        super().__init__(message, status_code=404)


def register_error_handlers(app):
    """Flask 앱에 에러 핸들러 등록"""

    @app.errorhandler(APIError)
    def handle_api_error(error):
        """사용자 정의 API 에러 핸들러"""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """HTTP 예외 핸들러"""
        return jsonify({
            'error': error.description,
            'status_code': error.code
        }), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """예상치 못한 에러 핸들러"""
        app.logger.error(f'Unexpected error: {str(error)}', exc_info=True)
        return jsonify({
            'error': '서버 오류가 발생했습니다',
            'status_code': 500
        }), 500

    @app.errorhandler(404)
    def handle_not_found(error):
        """404 에러 핸들러"""
        return jsonify({
            'error': '요청한 리소스를 찾을 수 없습니다',
            'status_code': 404
        }), 404

    @app.errorhandler(500)
    def handle_internal_error(error):
        """500 에러 핸들러"""
        app.logger.error(f'Internal server error: {str(error)}', exc_info=True)
        return jsonify({
            'error': '내부 서버 오류가 발생했습니다',
            'status_code': 500
        }), 500
