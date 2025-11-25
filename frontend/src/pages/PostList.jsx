import { useState, useEffect } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { getPosts } from '../services/posts'
import { isAuthenticated, getUser } from '../services/auth'
import './PostList.css'

/**
 * 게시글 목록 페이지 컴포넌트
 */
function PostList() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 20,
    total: 0
  })
  
  const categoryId = searchParams.get('category_id')
  const search = searchParams.get('search') || ''
  const currentPage = parseInt(searchParams.get('page') || '1')

  useEffect(() => {
    loadPosts()
  }, [categoryId, search, currentPage])

  /**
   * 게시글 목록 로드
   */
  const loadPosts = async () => {
    setLoading(true)
    setError('')
    try {
      const params = {
        page: currentPage,
        per_page: pagination.per_page,
      }
      if (categoryId) params.category_id = categoryId
      if (search) params.search = search

      const data = await getPosts(params)
      setPosts(data.posts || [])
      setPagination({
        page: data.page,
        per_page: data.per_page,
        total: data.total
      })
    } catch (err) {
      setError(err.response?.data?.error || '게시글을 불러오는데 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  /**
   * 검색 처리
   */
  const handleSearch = (e) => {
    e.preventDefault()
    const formData = new FormData(e.target)
    const searchValue = formData.get('search')
    setSearchParams({ search: searchValue, page: '1' })
  }

  /**
   * 페이지 변경
   */
  const handlePageChange = (newPage) => {
    setSearchParams({ ...Object.fromEntries(searchParams), page: newPage.toString() })
  }

  const totalPages = Math.ceil(pagination.total / pagination.per_page)
  const user = getUser()

  return (
    <div className="post-list-container">
      <div className="post-list-header">
        <h1>게시판</h1>
        {isAuthenticated() && (
          <Link to="/posts/new" className="write-button">
            글쓰기
          </Link>
        )}
      </div>

      {/* 검색 바 */}
      <form onSubmit={handleSearch} className="search-bar">
        <input
          type="text"
          name="search"
          placeholder="제목 또는 내용 검색..."
          defaultValue={search}
          className="search-input"
        />
        <button type="submit" className="search-button">검색</button>
      </form>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">로딩 중...</div>
      ) : posts.length === 0 ? (
        <div className="empty-state">게시글이 없습니다.</div>
      ) : (
        <>
          <div className="post-list">
            {posts.map((post) => (
              <Link key={post.id} to={`/posts/${post.id}`} className="post-item">
                <div className="post-header">
                  <h3 className="post-title">{post.title}</h3>
                  <span className="post-author">{post.author_nickname}</span>
                </div>
                <p className="post-content-preview">{post.content}</p>
                <div className="post-meta">
                  <span className="post-category">{post.category_name || '미분류'}</span>
                  <span className="post-date">{new Date(post.created_at).toLocaleDateString()}</span>
                  <span className="post-views">조회 {post.view_count}</span>
                  <span className="post-likes">좋아요 {post.like_count}</span>
                  <span className="post-comments">댓글 {post.comment_count}</span>
                </div>
              </Link>
            ))}
          </div>

          {/* 페이지네이션 */}
          {totalPages > 1 && (
            <div className="pagination">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
                className="page-button"
              >
                이전
              </button>
              {Array.from({ length: totalPages }, (_, i) => i + 1)
                .filter(page => {
                  // 현재 페이지 주변 5페이지만 표시
                  return Math.abs(page - currentPage) <= 2 || page === 1 || page === totalPages
                })
                .map((page, idx, arr) => {
                  // 생략 표시
                  if (idx > 0 && page - arr[idx - 1] > 1) {
                    return (
                      <span key={`ellipsis-${page}`} className="ellipsis">...</span>
                    )
                  }
                  return (
                    <button
                      key={page}
                      onClick={() => handlePageChange(page)}
                      className={`page-button ${currentPage === page ? 'active' : ''}`}
                    >
                      {page}
                    </button>
                  )
                })}
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
                className="page-button"
              >
                다음
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default PostList

