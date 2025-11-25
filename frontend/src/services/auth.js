/**
 * 인증 관련 API 서비스
 */
import api from './api'

/**
 * 일반 로그인
 */
export const login = async (email, password) => {
  const response = await api.post('/auth/login', { email, password })
  return response.data
}

/**
 * OAuth 로그인 URL 가져오기
 */
export const getOAuthUrl = async (provider) => {
  const response = await api.get(`/auth/oauth/${provider}`)
  return response.data.auth_url
}

/**
 * 토큰 저장
 */
export const saveToken = (token, user) => {
  localStorage.setItem('token', token)
  localStorage.setItem('user', JSON.stringify(user))
}

/**
 * 토큰 가져오기
 */
export const getToken = () => {
  return localStorage.getItem('token')
}

/**
 * 사용자 정보 가져오기
 */
export const getUser = () => {
  const userStr = localStorage.getItem('user')
  return userStr ? JSON.parse(userStr) : null
}

/**
 * 로그아웃
 */
export const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  window.location.href = '/login'
}

/**
 * 로그인 여부 확인
 */
export const isAuthenticated = () => {
  return !!getToken()
}

