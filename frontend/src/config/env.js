/**
 * 환경 변수 설정
 * Vite에서는 import.meta.env를 통해 환경 변수에 접근합니다.
 * VITE_ 접두사가 붙은 변수만 클라이언트에서 접근 가능합니다.
 */

const config = {
  // API 기본 URL
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  
  // OAuth 리다이렉트 URL
  KAKAO_REDIRECT_URI: import.meta.env.VITE_KAKAO_REDIRECT_URI || 'http://localhost:3000/auth/kakao/callback',
  NAVER_REDIRECT_URI: import.meta.env.VITE_NAVER_REDIRECT_URI || 'http://localhost:3000/auth/naver/callback',
  GOOGLE_REDIRECT_URI: import.meta.env.VITE_GOOGLE_REDIRECT_URI || 'http://localhost:3000/auth/google/callback',
  
  // 개발 모드 여부
  IS_DEV: import.meta.env.DEV,
}

export default config

