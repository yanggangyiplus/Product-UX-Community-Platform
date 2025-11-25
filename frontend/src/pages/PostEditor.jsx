import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getPost, createPost, updatePost } from '../services/posts'
import { isAuthenticated } from '../services/auth'
import './PostEditor.css'

/**
 * 게시글 작성/수정 페이지 컴포넌트
 */
function PostEditor() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEditMode = !!id

  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [categoryId, setCategoryId] = useState('')
  const [status, setStatus] = useState('published')
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/login')
      return
    }

    if (isEditMode) {
      loadPost()
    }
  }, [id, navigate])

  /**
   * 게시글 로드 (수정 모드)
   */
  const loadPost = async () => {
    try {
      const data = await getPost(id)
      setTitle(data.title)
      setContent(data.content)
      setCategoryId(data.category_id || '')
      setStatus(data.status === 'draft' ? 'draft' : 'published')
    } catch (err) {
      setError(err.response?.data?.error || '게시글을 불러오는데 실패했습니다.')
    }
  }

  /**
   * 게시글 저장
   */
  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!title.trim() || !content.trim()) {
      setError('제목과 내용을 입력해주세요.')
      return
    }

    setLoading(true)
    setError('')

    try {
      const postData = {
        title,
        content,
        category_id: categoryId ? parseInt(categoryId) : null,
        status
      }

      if (isEditMode) {
        await updatePost(id, postData)
      } else {
        const result = await createPost(postData)
        navigate(`/posts/${result.id}`)
        return
      }

      navigate(`/posts/${id}`)
    } catch (err) {
      setError(err.response?.data?.error || '게시글 저장에 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  /**
   * 임시저장
   */
  const handleSaveDraft = async () => {
    setSaving(true)
    setError('')

    try {
      const postData = {
        title: title || '제목 없음',
        content: content || '',
        category_id: categoryId ? parseInt(categoryId) : null,
        status: 'draft'
      }

      if (isEditMode) {
        await updatePost(id, postData)
      } else {
        const result = await createPost(postData)
        navigate(`/posts/${result.id}`)
        return
      }

      alert('임시저장되었습니다.')
    } catch (err) {
      setError(err.response?.data?.error || '임시저장에 실패했습니다.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="post-editor-container">
      <div className="post-editor-header">
        <h1>{isEditMode ? '게시글 수정' : '게시글 작성'}</h1>
        <div className="editor-actions">
          <button
            onClick={handleSaveDraft}
            disabled={saving}
            className="draft-button"
          >
            {saving ? '저장 중...' : '임시저장'}
          </button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit} className="post-editor-form">
        <div className="form-group">
          <label htmlFor="category">카테고리</label>
          <select
            id="category"
            value={categoryId}
            onChange={(e) => setCategoryId(e.target.value)}
            className="form-input"
          >
            <option value="">선택 안함</option>
            {/* 카테고리 목록은 추후 API로 가져올 수 있음 */}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="title">제목 *</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="제목을 입력하세요"
            className="form-input"
            required
            maxLength={500}
          />
          <span className="char-count">{title.length}/500</span>
        </div>

        <div className="form-group">
          <label htmlFor="content">내용 *</label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="내용을 입력하세요"
            className="form-textarea"
            rows="20"
            required
          />
          <span className="char-count">{content.length}자</span>
        </div>

        <div className="form-group">
          <label>
            <input
              type="radio"
              value="published"
              checked={status === 'published'}
              onChange={(e) => setStatus(e.target.value)}
            />
            바로 게시
          </label>
          <label>
            <input
              type="radio"
              value="draft"
              checked={status === 'draft'}
              onChange={(e) => setStatus(e.target.value)}
            />
            임시저장
          </label>
        </div>

        <div className="form-actions">
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="cancel-button"
          >
            취소
          </button>
          <button
            type="submit"
            disabled={loading}
            className="submit-button"
          >
            {loading ? '저장 중...' : isEditMode ? '수정하기' : '게시하기'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default PostEditor

