import { useState, useEffect } from 'react'
import { getUsers, updateUser } from '../../services/admin'
import './AdminPages.css'

/**
 * 회원 관리 페이지 컴포넌트
 */
function UserManagement() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [search, setSearch] = useState('')
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 20,
    total: 0
  })

  useEffect(() => {
    loadUsers()
  }, [search, pagination.page])

  /**
   * 회원 목록 로드
   */
  const loadUsers = async () => {
    setLoading(true)
    setError('')
    try {
      const params = {
        page: pagination.page,
        per_page: pagination.per_page
      }
      if (search) params.search = search

      const data = await getUsers(params)
      setUsers(data.users || [])
      setPagination({
        page: data.page,
        per_page: data.per_page,
        total: data.total
      })
    } catch (err) {
      setError(err.response?.data?.error || '회원 목록을 불러오는데 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  /**
   * 회원 상태 변경
   */
  const handleUserStatusChange = async (userId, isActive) => {
    try {
      await updateUser(userId, { is_active: isActive })
      loadUsers()
    } catch (err) {
      alert(err.response?.data?.error || '회원 상태 변경에 실패했습니다.')
    }
  }

  /**
   * 회원 역할 변경
   */
  const handleRoleChange = async (userId, role) => {
    if (!window.confirm(`회원 역할을 "${role === 'admin' ? '관리자' : '일반회원'}"로 변경하시겠습니까?`)) {
      return
    }

    try {
      await updateUser(userId, { role })
      loadUsers()
    } catch (err) {
      alert(err.response?.data?.error || '회원 역할 변경에 실패했습니다.')
    }
  }

  /**
   * 검색 처리
   */
  const handleSearch = (e) => {
    e.preventDefault()
    const formData = new FormData(e.target)
    setSearch(formData.get('search'))
    setPagination({ ...pagination, page: 1 })
  }

  return (
    <div className="admin-page">
      <div className="admin-page-header">
        <h1>회원 관리</h1>
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            name="search"
            placeholder="이메일 또는 닉네임 검색..."
            className="search-input"
          />
          <button type="submit" className="search-button">검색</button>
        </form>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">로딩 중...</div>
      ) : users.length === 0 ? (
        <div className="empty-state">회원이 없습니다.</div>
      ) : (
        <div className="admin-table-container">
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>이메일</th>
                <th>닉네임</th>
                <th>역할</th>
                <th>상태</th>
                <th>가입일시</th>
                <th>관리</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.email || '-'}</td>
                  <td>{user.nickname}</td>
                  <td>
                    <select
                      value={user.role}
                      onChange={(e) => handleRoleChange(user.id, e.target.value)}
                      className="role-select"
                    >
                      <option value="user">일반회원</option>
                      <option value="admin">관리자</option>
                    </select>
                  </td>
                  <td>
                    <span className={`status-badge ${user.is_active ? 'status-active' : 'status-inactive'}`}>
                      {user.is_active ? '활성' : '비활성'}
                    </span>
                  </td>
                  <td>{new Date(user.created_at).toLocaleString()}</td>
                  <td>
                    <button
                      onClick={() => handleUserStatusChange(user.id, !user.is_active)}
                      className={`action-btn ${user.is_active ? 'deactivate-btn' : 'activate-btn'}`}
                    >
                      {user.is_active ? '비활성화' : '활성화'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default UserManagement

