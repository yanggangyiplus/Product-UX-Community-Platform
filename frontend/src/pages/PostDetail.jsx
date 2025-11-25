import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { getPost, deletePost, likePost } from '../services/posts'
import { getComments, createComment, deleteComment } from '../services/comments'
import { getUser, isAuthenticated } from '../services/auth'
import './PostDetail.css'

/**
 * 게시글 상세 페이지 컴포넌트
 */
function PostDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [post, setPost] = useState(null)
  const [comments, setComments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [commentContent, setCommentContent] = useState('')
  const [submittingComment, setSubmittingComment] = useState(false)
  const [liked, setLiked] = useState(false)

  const user = getUser()

  useEffect(() => {
    loadPost()
    loadComments()
  }, [id])

  /**
   * 게시글 로드
   */
  const loadPost = async () => {
    try {
      const data = await getPost(id)
      setPost(data)
    } catch (err) {
      setError(err.response?.data?.error || '게시글을 불러오는데 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  /**
   * 댓글 목록 로드
   */
  const loadComments = async () => {
    try {
      const data = await getComments(id)
      setComments(data.comments || [])
    } catch (err) {
      console.error('댓글 로드 실패:', err)
    }
  }

  /**
   * 댓글 작성
   */
  const handleSubmitComment = async (e) => {
    e.preventDefault()
    if (!isAuthenticated()) {
      navigate('/login')
      return
    }

    setSubmittingComment(true)
    try {
      await createComment({
        post_id: parseInt(id),
        content: commentContent
      })
      setCommentContent('')
      loadComments()
    } catch (err) {
      alert(err.response?.data?.error || '댓글 작성에 실패했습니다.')
    } finally {
      setSubmittingComment(false)
    }
  }

  /**
   * 댓글 삭제
   */
  const handleDeleteComment = async (commentId) => {
    if (!window.confirm('댓글을 삭제하시겠습니까?')) return

    try {
      await deleteComment(commentId)
      loadComments()
    } catch (err) {
      alert(err.response?.data?.error || '댓글 삭제에 실패했습니다.')
    }
  }

  /**
   * 게시글 삭제
   */
  const handleDeletePost = async () => {
    if (!window.confirm('게시글을 삭제하시겠습니까?')) return

    try {
      await deletePost(id)
      navigate('/posts')
    } catch (err) {
      alert(err.response?.data?.error || '게시글 삭제에 실패했습니다.')
    }
  }

  /**
   * 좋아요 처리
   */
  const handleLike = async () => {
    if (!isAuthenticated()) {
      navigate('/login')
      return
    }

    try {
      const data = await likePost(id)
      setLiked(!liked)
      if (post) {
        setPost({ ...post, like_count: data.like_count })
      }
    } catch (err) {
      alert(err.response?.data?.error || '좋아요 처리에 실패했습니다.')
    }
  }

  /**
   * 댓글 렌더링 (재귀적)
   */
  const renderComments = (commentList, depth = 0) => {
    return commentList.map((comment) => (
      <div key={comment.id} className={`comment-item ${depth > 0 ? 'reply' : ''}`}>
        <div className="comment-header">
          <span className="comment-author">{comment.author_nickname}</span>
          <span className="comment-date">
            {new Date(comment.created_at).toLocaleString()}
          </span>
          {user && user.id === comment.author_id && (
            <button
              onClick={() => handleDeleteComment(comment.id)}
              className="comment-delete-btn"
            >
              삭제
            </button>
          )}
        </div>
        <div className="comment-content">{comment.content}</div>
        {comment.replies && comment.replies.length > 0 && (
          <div className="comment-replies">
            {renderComments(comment.replies, depth + 1)}
          </div>
        )}
      </div>
    ))
  }

  if (loading) {
    return <div className="loading">로딩 중...</div>
  }

  if (error || !post) {
    return <div className="error-message">{error || '게시글을 찾을 수 없습니다.'}</div>
  }

  const isAuthor = user && user.id === post.author_id

  return (
    <div className="post-detail-container">
      <div className="post-detail-header">
        <Link to="/posts" className="back-button">← 목록으로</Link>
        {isAuthor && (
          <div className="post-actions">
            <Link to={`/posts/${id}/edit`} className="edit-button">수정</Link>
            <button onClick={handleDeletePost} className="delete-button">삭제</button>
          </div>
        )}
      </div>

      <article className="post-detail">
        <div className="post-header">
          <h1 className="post-title">{post.title}</h1>
          <div className="post-meta">
            <span className="post-author">{post.author_nickname}</span>
            <span className="post-date">{new Date(post.created_at).toLocaleString()}</span>
            <span className="post-category">{post.category_name || '미분류'}</span>
          </div>
        </div>

        {post.images && post.images.length > 0 && (
          <div className="post-images">
            {post.images.map((imageUrl, idx) => (
              <img key={idx} src={imageUrl} alt={`${post.title} ${idx + 1}`} />
            ))}
          </div>
        )}

        <div className="post-content" dangerouslySetInnerHTML={{ __html: post.content }} />

        <div className="post-footer">
          <button onClick={handleLike} className={`like-button ${liked ? 'liked' : ''}`}>
            좋아요 {post.like_count}
          </button>
          <span className="post-stats">
            조회 {post.view_count} | 댓글 {post.comment_count}
          </span>
        </div>
      </article>

      {/* 댓글 섹션 */}
      <section className="comments-section">
        <h2>댓글 ({comments.length})</h2>

        {isAuthenticated() && (
          <form onSubmit={handleSubmitComment} className="comment-form">
            <textarea
              value={commentContent}
              onChange={(e) => setCommentContent(e.target.value)}
              placeholder="댓글을 입력하세요..."
              rows="4"
              required
            />
            <button type="submit" disabled={submittingComment}>
              {submittingComment ? '작성 중...' : '댓글 작성'}
            </button>
          </form>
        )}

        <div className="comments-list">
          {comments.length === 0 ? (
            <div className="empty-comments">댓글이 없습니다.</div>
          ) : (
            renderComments(comments)
          )}
        </div>
      </section>
    </div>
  )
}

export default PostDetail

