import { useState } from 'react'
import './AdminPages.css'

/**
 * 카테고리 관리 페이지 컴포넌트
 */
function CategoryManagement() {
  const [categories, setCategories] = useState([])
  const [newCategoryName, setNewCategoryName] = useState('')
  const [newCategoryDesc, setNewCategoryDesc] = useState('')
  const [editingId, setEditingId] = useState(null)

  // TODO: API 연동 필요
  // 현재는 UI만 구현

  /**
   * 카테고리 추가
   */
  const handleAddCategory = () => {
    if (!newCategoryName.trim()) {
      alert('카테고리 이름을 입력해주세요.')
      return
    }

    const newCategory = {
      id: Date.now(),
      name: newCategoryName,
      description: newCategoryDesc,
      order: categories.length + 1,
      is_active: true
    }

    setCategories([...categories, newCategory])
    setNewCategoryName('')
    setNewCategoryDesc('')
  }

  /**
   * 카테고리 수정
   */
  const handleUpdateCategory = (id, name, description) => {
    setCategories(categories.map(cat =>
      cat.id === id ? { ...cat, name, description } : cat
    ))
    setEditingId(null)
  }

  /**
   * 카테고리 삭제
   */
  const handleDeleteCategory = (id) => {
    if (!window.confirm('카테고리를 삭제하시겠습니까?')) return
    setCategories(categories.filter(cat => cat.id !== id))
  }

  /**
   * 카테고리 활성화/비활성화
   */
  const handleToggleActive = (id) => {
    setCategories(categories.map(cat =>
      cat.id === id ? { ...cat, is_active: !cat.is_active } : cat
    ))
  }

  return (
    <div className="admin-page">
      <div className="admin-page-header">
        <h1>카테고리 관리</h1>
      </div>

      <div className="category-form">
        <h2>카테고리 추가</h2>
        <div className="form-row">
          <input
            type="text"
            placeholder="카테고리 이름"
            value={newCategoryName}
            onChange={(e) => setNewCategoryName(e.target.value)}
            className="form-input"
          />
          <input
            type="text"
            placeholder="설명 (선택사항)"
            value={newCategoryDesc}
            onChange={(e) => setNewCategoryDesc(e.target.value)}
            className="form-input"
          />
          <button onClick={handleAddCategory} className="add-button">
            추가
          </button>
        </div>
      </div>

      <div className="admin-table-container">
        <table className="admin-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>이름</th>
              <th>설명</th>
              <th>순서</th>
              <th>상태</th>
              <th>관리</th>
            </tr>
          </thead>
          <tbody>
            {categories.length === 0 ? (
              <tr>
                <td colSpan="6" className="empty-state">카테고리가 없습니다.</td>
              </tr>
            ) : (
              categories.map((category) => (
                <tr key={category.id}>
                  <td>{category.id}</td>
                  <td>
                    {editingId === category.id ? (
                      <input
                        type="text"
                        defaultValue={category.name}
                        onBlur={(e) => handleUpdateCategory(category.id, e.target.value, category.description)}
                        className="inline-input"
                      />
                    ) : (
                      <span onClick={() => setEditingId(category.id)} className="editable-text">
                        {category.name}
                      </span>
                    )}
                  </td>
                  <td>
                    {editingId === category.id ? (
                      <input
                        type="text"
                        defaultValue={category.description}
                        onBlur={(e) => handleUpdateCategory(category.id, category.name, e.target.value)}
                        className="inline-input"
                      />
                    ) : (
                      <span onClick={() => setEditingId(category.id)} className="editable-text">
                        {category.description || '-'}
                      </span>
                    )}
                  </td>
                  <td>{category.order}</td>
                  <td>
                    <span className={`status-badge ${category.is_active ? 'status-active' : 'status-inactive'}`}>
                      {category.is_active ? '활성' : '비활성'}
                    </span>
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button
                        onClick={() => handleToggleActive(category.id)}
                        className={`action-btn ${category.is_active ? 'deactivate-btn' : 'activate-btn'}`}
                      >
                        {category.is_active ? '비활성화' : '활성화'}
                      </button>
                      <button
                        onClick={() => handleDeleteCategory(category.id)}
                        className="action-btn delete-btn"
                      >
                        삭제
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default CategoryManagement

