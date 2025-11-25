import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { login, getOAuthUrl, saveToken, isAuthenticated } from '../services/auth'
import './Login.css'

/**
 * 로그인 페이지 컴포넌트
 * 일반 로그인 및 OAuth 로그인 지원
 */
function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    // 이미 로그인된 경우 리다이렉트
    if (isAuthenticated()) {
      navigate('/')
    }
  }, [navigate])

  /**
   * 일반 로그인 처리
   */
  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const data = await login(email, password)
      saveToken(data.token, data.user)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.error || '로그인에 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  /**
   * OAuth 로그인 처리
   */
  const handleOAuthLogin = async (provider) => {
    try {
      const authUrl = await getOAuthUrl(provider)
      // OAuth 제공자 페이지로 리다이렉트
      window.location.href = authUrl
    } catch (err) {
      setError(err.response?.data?.error || `${provider} 로그인에 실패했습니다.`)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">로그인</h1>
        
        {error && <div className="error-message">{error}</div>}

        {/* OAuth 로그인 버튼 */}
        <div className="oauth-buttons">
          <button
            type="button"
            className="oauth-button kakao"
            onClick={() => handleOAuthLogin('kakao')}
            disabled={loading}
          >
            <span className="oauth-icon">카카오</span>
            카카오로 시작하기
          </button>
          
          <button
            type="button"
            className="oauth-button naver"
            onClick={() => handleOAuthLogin('naver')}
            disabled={loading}
          >
            <span className="oauth-icon">네이버</span>
            네이버로 시작하기
          </button>
          
          <button
            type="button"
            className="oauth-button google"
            onClick={() => handleOAuthLogin('google')}
            disabled={loading}
          >
            <span className="oauth-icon">구글</span>
            구글로 시작하기
          </button>
        </div>

        <div className="divider">
          <span>또는</span>
        </div>

        {/* 일반 로그인 폼 */}
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">이메일</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="이메일을 입력하세요"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">비밀번호</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="비밀번호를 입력하세요"
              required
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >
            {loading ? '로그인 중...' : '로그인'}
          </button>
        </form>

        <div className="login-footer">
          <a href="/signup">회원가입</a>
          <span>|</span>
          <a href="/forgot-password">비밀번호 찾기</a>
        </div>
      </div>
    </div>
  )
}

export default Login

