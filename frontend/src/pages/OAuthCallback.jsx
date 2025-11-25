import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { saveToken } from '../services/auth'
import './OAuthCallback.css'

/**
 * OAuth 콜백 페이지 컴포넌트
 * OAuth 인증 후 리다이렉트 처리
 */
function OAuthCallback() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()

  useEffect(() => {
    const token = searchParams.get('token')
    const provider = searchParams.get('provider')
    const error = searchParams.get('error')

    if (error) {
      // 에러 발생 시 로그인 페이지로 리다이렉트
      navigate(`/login?error=${encodeURIComponent(error)}`)
      return
    }

    if (token) {
      // 토큰이 있으면 저장하고 홈으로 리다이렉트
      // 사용자 정보는 백엔드에서 추가로 가져와야 할 수 있음
      saveToken(token, {}) // 임시로 빈 객체 저장
      navigate('/')
    } else {
      // 토큰이 없으면 로그인 페이지로 리다이렉트
      navigate('/login?error=인증에 실패했습니다.')
    }
  }, [searchParams, navigate])

  return (
    <div className="callback-container">
      <div className="callback-card">
        <div className="spinner"></div>
        <p>로그인 처리 중...</p>
      </div>
    </div>
  )
}

export default OAuthCallback

