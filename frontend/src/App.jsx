import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
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
          <Route path="/" element={<div>Home</div>} />
          <Route path="/login" element={<div>Login</div>} />
          <Route path="/board" element={<div>Board</div>} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

