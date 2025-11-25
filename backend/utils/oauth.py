"""
OAuth 관련 유틸리티 함수
카카오, 네이버, 구글 OAuth 처리
"""
import os
import requests
from urllib.parse import urlencode


def get_kakao_auth_url():
    """카카오 OAuth 인증 URL 생성"""
    client_id = os.getenv('KAKAO_CLIENT_ID', '')
    redirect_uri = os.getenv('KAKAO_REDIRECT_URI', '')
    
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code'
    }
    
    return f"https://kauth.kakao.com/oauth/authorize?{urlencode(params)}"


def get_naver_auth_url(state):
    """네이버 OAuth 인증 URL 생성"""
    client_id = os.getenv('NAVER_CLIENT_ID', '')
    redirect_uri = os.getenv('NAVER_REDIRECT_URI', '')
    
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'state': state
    }
    
    return f"https://nid.naver.com/oauth2.0/authorize?{urlencode(params)}"


def get_google_auth_url(state):
    """구글 OAuth 인증 URL 생성"""
    client_id = os.getenv('GOOGLE_CLIENT_ID', '')
    redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', '')
    
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state
    }
    
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"


def get_kakao_token(code):
    """카카오 OAuth 토큰 교환"""
    client_id = os.getenv('KAKAO_CLIENT_ID', '')
    client_secret = os.getenv('KAKAO_CLIENT_SECRET', '')
    redirect_uri = os.getenv('KAKAO_REDIRECT_URI', '')
    
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': code
    }
    
    response = requests.post('https://kauth.kakao.com/oauth/token', data=data)
    return response.json() if response.status_code == 200 else None


def get_naver_token(code, state):
    """네이버 OAuth 토큰 교환"""
    client_id = os.getenv('NAVER_CLIENT_ID', '')
    client_secret = os.getenv('NAVER_CLIENT_SECRET', '')
    redirect_uri = os.getenv('NAVER_REDIRECT_URI', '')
    
    params = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': code,
        'state': state
    }
    
    response = requests.get('https://nid.naver.com/oauth2.0/token', params=params)
    return response.json() if response.status_code == 200 else None


def get_google_token(code):
    """구글 OAuth 토큰 교환"""
    client_id = os.getenv('GOOGLE_CLIENT_ID', '')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET', '')
    redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', '')
    
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': code
    }
    
    response = requests.post('https://oauth2.googleapis.com/token', data=data)
    return response.json() if response.status_code == 200 else None


def get_kakao_user_info(access_token):
    """카카오 사용자 정보 가져오기"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
    return response.json() if response.status_code == 200 else None


def get_naver_user_info(access_token):
    """네이버 사용자 정보 가져오기"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://openapi.naver.com/v1/nid/me', headers=headers)
    return response.json() if response.status_code == 200 else None


def get_google_user_info(access_token):
    """구글 사용자 정보 가져오기"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
    return response.json() if response.status_code == 200 else None

