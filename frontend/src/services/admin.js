/**
 * 관리자 관련 API 서비스
 */
import api from './api'

/**
 * 신고 목록 조회
 */
export const getReports = async (params = {}) => {
  const response = await api.get('/admin/reports', { params })
  return response.data
}

/**
 * 신고 상태 변경
 */
export const updateReportStatus = async (reportId, data) => {
  const response = await api.put(`/admin/reports/${reportId}`, data)
  return response.data
}

/**
 * 회원 목록 조회
 */
export const getUsers = async (params = {}) => {
  const response = await api.get('/admin/users', { params })
  return response.data
}

/**
 * 회원 정보 수정
 */
export const updateUser = async (userId, data) => {
  const response = await api.put(`/admin/users/${userId}`, data)
  return response.data
}

/**
 * 게시글 목록 조회 (관리자용)
 */
export const getAllPosts = async (params = {}) => {
  const response = await api.get('/admin/posts', { params })
  return response.data
}

/**
 * 게시글 삭제 (관리자)
 */
export const deletePostAdmin = async (postId) => {
  const response = await api.delete(`/admin/posts/${postId}`)
  return response.data
}

