import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import OAuthCallback from './pages/OAuthCallback'
import PostList from './pages/PostList'
import PostDetail from './pages/PostDetail'
import PostEditor from './pages/PostEditor'
import AdminLayout from './pages/admin/AdminLayout'
import ReportList from './pages/admin/ReportList'
import UserManagement from './pages/admin/UserManagement'
import CategoryManagement from './pages/admin/CategoryManagement'
import './App.css'

/**
 * 메인 App 컴포넌트
 * 라우팅 설정 및 전체 앱 구조 관리
 */
function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<PostList />} />
          <Route path="/posts" element={<PostList />} />
          <Route path="/posts/new" element={<PostEditor />} />
          <Route path="/posts/:id" element={<PostDetail />} />
          <Route path="/posts/:id/edit" element={<PostEditor />} />
          <Route path="/login" element={<Login />} />
          <Route path="/auth/callback" element={<OAuthCallback />} />
          <Route path="/admin" element={<AdminLayout />}>
            <Route path="reports" element={<ReportList />} />
            <Route path="users" element={<UserManagement />} />
            <Route path="categories" element={<CategoryManagement />} />
          </Route>
        </Routes>
      </div>
    </Router>
  )
}

export default App

