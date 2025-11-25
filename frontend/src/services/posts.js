/**
 * 게시글 관련 API 서비스
 */
import api from './api'

/**
 * 게시글 목록 조회
 */
export const getPosts = async (params = {}) => {
  const response = await api.get('/posts', { params })
  return response.data
}

/**
 * 게시글 상세 조회
 */
export const getPost = async (postId) => {
  const response = await api.get(`/posts/${postId}`)
  return response.data
}

/**
 * 게시글 작성
 */
export const createPost = async (data) => {
  const response = await api.post('/posts', data)
  return response.data
}

/**
 * 게시글 수정
 */
export const updatePost = async (postId, data) => {
  const response = await api.put(`/posts/${postId}`, data)
  return response.data
}

/**
 * 게시글 삭제
 */
export const deletePost = async (postId) => {
  const response = await api.delete(`/posts/${postId}`)
  return response.data
}

/**
 * 게시글 좋아요
 */
export const likePost = async (postId) => {
  const response = await api.post(`/posts/${postId}/like`)
  return response.data
}

