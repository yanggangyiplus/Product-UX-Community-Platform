/**
 * 댓글 관련 API 서비스
 */
import api from './api'

/**
 * 댓글 목록 조회
 */
export const getComments = async (postId) => {
  const response = await api.get('/comments', { params: { post_id: postId } })
  return response.data
}

/**
 * 댓글 작성
 */
export const createComment = async (data) => {
  const response = await api.post('/comments', data)
  return response.data
}

/**
 * 댓글 수정
 */
export const updateComment = async (commentId, data) => {
  const response = await api.put(`/comments/${commentId}`, data)
  return response.data
}

/**
 * 댓글 삭제
 */
export const deleteComment = async (commentId) => {
  const response = await api.delete(`/comments/${commentId}`)
  return response.data
}

