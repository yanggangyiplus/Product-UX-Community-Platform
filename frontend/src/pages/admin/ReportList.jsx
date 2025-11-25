import { useState, useEffect } from 'react'
import { getReports, updateReportStatus } from '../../services/admin'
import './AdminPages.css'

/**
 * 신고 관리 페이지 컴포넌트
 */
function ReportList() {
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [statusFilter, setStatusFilter] = useState('pending')
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 20,
    total: 0
  })

  useEffect(() => {
    loadReports()
  }, [statusFilter, pagination.page])

  /**
   * 신고 목록 로드
   */
  const loadReports = async () => {
    setLoading(true)
    setError('')
    try {
      const data = await getReports({
        status: statusFilter,
        page: pagination.page,
        per_page: pagination.per_page
      })
      setReports(data.reports || [])
      setPagination({
        page: data.page,
        per_page: data.per_page,
        total: data.total
      })
    } catch (err) {
      setError(err.response?.data?.error || '신고 목록을 불러오는데 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  /**
   * 신고 상태 변경
   */
  const handleStatusChange = async (reportId, newStatus, adminNote = '') => {
    if (!window.confirm(`신고 상태를 "${getStatusLabel(newStatus)}"로 변경하시겠습니까?`)) {
      return
    }

    try {
      await updateReportStatus(reportId, {
        status: newStatus,
        admin_note: adminNote
      })
      loadReports()
    } catch (err) {
      alert(err.response?.data?.error || '신고 상태 변경에 실패했습니다.')
    }
  }

  /**
   * 상태 라벨 가져오기
   */
  const getStatusLabel = (status) => {
    const labels = {
      pending: '대기',
      processing: '처리중',
      resolved: '완료',
      rejected: '거부'
    }
    return labels[status] || status
  }

  /**
   * 유형 라벨 가져오기
   */
  const getTypeLabel = (type) => {
    return type === 'post' ? '게시글' : '댓글'
  }

  return (
    <div className="admin-page">
      <div className="admin-page-header">
        <h1>신고 관리</h1>
        <div className="filter-buttons">
          {['pending', 'processing', 'resolved', 'rejected'].map((status) => (
            <button
              key={status}
              onClick={() => {
                setStatusFilter(status)
                setPagination({ ...pagination, page: 1 })
              }}
              className={`filter-button ${statusFilter === status ? 'active' : ''}`}
            >
              {getStatusLabel(status)}
            </button>
          ))}
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">로딩 중...</div>
      ) : reports.length === 0 ? (
        <div className="empty-state">신고가 없습니다.</div>
      ) : (
        <div className="admin-table-container">
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>유형</th>
                <th>대상</th>
                <th>신고자</th>
                <th>사유</th>
                <th>상태</th>
                <th>신고일시</th>
                <th>처리</th>
              </tr>
            </thead>
            <tbody>
              {reports.map((report) => (
                <tr key={report.id}>
                  <td>{report.id}</td>
                  <td>{getTypeLabel(report.report_type)}</td>
                  <td>
                    {report.post_id ? `게시글 #${report.post_id}` : `댓글 #${report.comment_id}`}
                  </td>
                  <td>{report.reporter_nickname}</td>
                  <td className="reason-cell">{report.reason}</td>
                  <td>
                    <span className={`status-badge status-${report.status}`}>
                      {getStatusLabel(report.status)}
                    </span>
                  </td>
                  <td>{new Date(report.created_at).toLocaleString()}</td>
                  <td>
                    {report.status === 'pending' && (
                      <div className="action-buttons">
                        <button
                          onClick={() => handleStatusChange(report.id, 'processing')}
                          className="action-btn process-btn"
                        >
                          처리중
                        </button>
                        <button
                          onClick={() => handleStatusChange(report.id, 'resolved')}
                          className="action-btn resolve-btn"
                        >
                          완료
                        </button>
                        <button
                          onClick={() => handleStatusChange(report.id, 'rejected')}
                          className="action-btn reject-btn"
                        >
                          거부
                        </button>
                      </div>
                    )}
                    {report.status === 'processing' && (
                      <div className="action-buttons">
                        <button
                          onClick={() => handleStatusChange(report.id, 'resolved')}
                          className="action-btn resolve-btn"
                        >
                          완료
                        </button>
                        <button
                          onClick={() => handleStatusChange(report.id, 'rejected')}
                          className="action-btn reject-btn"
                        >
                          거부
                        </button>
                      </div>
                    )}
                    {report.admin_note && (
                      <div className="admin-note">처리사유: {report.admin_note}</div>
                    )}
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

export default ReportList

