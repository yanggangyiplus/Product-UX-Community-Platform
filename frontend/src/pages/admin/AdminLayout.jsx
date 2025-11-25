import { useState } from 'react'
import { Link, Outlet, useLocation } from 'react-router-dom'
import { getUser } from '../../services/auth'
import './AdminLayout.css'

/**
 * 관리자 레이아웃 컴포넌트
 */
function AdminLayout() {
  const location = useLocation()
  const user = getUser()

  // 관리자 권한 확인
  if (!user || user.role !== 'admin') {
    return (
      <div className="admin-error">
        <h2>접근 권한이 없습니다.</h2>
        <p>관리자만 접근할 수 있습니다.</p>
        <Link to="/">홈으로 돌아가기</Link>
      </div>
    )
  }

  const menuItems = [
    { path: '/admin/reports', label: '신고 관리' },
    { path: '/admin/users', label: '회원 관리' },
    { path: '/admin/categories', label: '카테고리 관리' },
    { path: '/admin/posts', label: '게시글 관리' },
  ]

  return (
    <div className="admin-layout">
      <div className="admin-sidebar">
        <h2 className="admin-title">관리자 페이지</h2>
        <nav className="admin-nav">
          {menuItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`admin-nav-item ${
                location.pathname === item.path ? 'active' : ''
              }`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
      <div className="admin-content">
        <Outlet />
      </div>
    </div>
  )
}

export default AdminLayout

