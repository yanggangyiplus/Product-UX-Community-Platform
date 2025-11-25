"""
관리자 관련 API 라우트
/admin/* 엔드포인트 포함
"""
from flask import Blueprint, request, jsonify
from database import SessionLocal
from models import Report, ReportStatus, User, Post, Comment, UserRole, PostStatus
from utils.auth import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


@admin_bp.route('/reports', methods=['GET'])
@admin_required
def get_reports():
    """신고 목록 조회"""
    status = request.args.get('status', 'pending')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    db = SessionLocal()
    try:
        query = db.query(Report)
        
        if status:
            query = query.filter(Report.status == ReportStatus[status.upper()])
        
        reports = query.order_by(Report.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
        total = query.count()
        
        return jsonify({
            'reports': [{
                'id': report.id,
                'report_type': report.report_type.value,
                'post_id': report.post_id,
                'comment_id': report.comment_id,
                'reason': report.reason,
                'status': report.status.value,
                'reporter_id': report.reporter_id,
                'reporter_nickname': report.reporter.nickname,
                'admin_note': report.admin_note,
                'processed_by': report.processed_by,
                'processed_at': report.processed_at.isoformat() if report.processed_at else None,
                'created_at': report.created_at.isoformat()
            } for report in reports],
            'total': total,
            'page': page,
            'per_page': per_page
        }), 200
    finally:
        db.close()


@admin_bp.route('/reports/<int:report_id>', methods=['PUT'])
@admin_required
def update_report_status(report_id):
    """신고 상태 변경"""
    data = request.get_json()
    status = data.get('status')
    admin_note = data.get('admin_note', '')
    
    if not status or status not in ['pending', 'processing', 'resolved', 'rejected']:
        return jsonify({'error': '유효한 상태를 입력해주세요.'}), 400
    
    db = SessionLocal()
    try:
        report = db.query(Report).filter(Report.id == report_id).first()
        
        if not report:
            return jsonify({'error': '신고를 찾을 수 없습니다.'}), 404
        
        report.status = ReportStatus[status.upper()]
        report.admin_note = admin_note
        report.processed_by = request.current_user_id
        
        from datetime import datetime
        report.processed_at = datetime.utcnow()
        
        db.commit()
        
        return jsonify({'message': '신고 상태가 변경되었습니다.'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'신고 상태 변경 중 오류가 발생했습니다: {str(e)}'}), 500
    finally:
        db.close()


@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    """회원 목록 조회"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    db = SessionLocal()
    try:
        query = db.query(User)
        
        if search:
            query = query.filter(
                User.email.contains(search) | User.nickname.contains(search)
            )
        
        users = query.order_by(User.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
        total = query.count()
        
        return jsonify({
            'users': [{
                'id': user.id,
                'email': user.email,
                'nickname': user.nickname,
                'role': user.role.value,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat()
            } for user in users],
            'total': total,
            'page': page,
            'per_page': per_page
        }), 200
    finally:
        db.close()


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """회원 정보 수정"""
    data = request.get_json()
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return jsonify({'error': '회원을 찾을 수 없습니다.'}), 404
        
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'role' in data:
            user.role = UserRole[data['role'].upper()]
        
        db.commit()
        
        return jsonify({'message': '회원 정보가 수정되었습니다.'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'회원 정보 수정 중 오류가 발생했습니다: {str(e)}'}), 500
    finally:
        db.close()


@admin_bp.route('/posts', methods=['GET'])
@admin_required
def get_all_posts():
    """모든 게시글 조회 (관리자용)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    
    db = SessionLocal()
    try:
        query = db.query(Post)
        
        if status:
            query = query.filter(Post.status == PostStatus[status.upper()])
        
        posts = query.order_by(Post.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
        total = query.count()
        
        return jsonify({
            'posts': [{
                'id': post.id,
                'title': post.title,
                'author_id': post.author_id,
                'author_nickname': post.author.nickname,
                'status': post.status.value,
                'view_count': post.view_count,
                'like_count': post.like_count,
                'comment_count': post.comment_count,
                'created_at': post.created_at.isoformat()
            } for post in posts],
            'total': total,
            'page': page,
            'per_page': per_page
        }), 200
    finally:
        db.close()


@admin_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@admin_required
def delete_post_admin(post_id):
    """게시글 삭제 (관리자)"""
    db = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        
        if not post:
            return jsonify({'error': '게시글을 찾을 수 없습니다.'}), 404
        
        post.status = PostStatus.DELETED
        db.commit()
        
        return jsonify({'message': '게시글이 삭제되었습니다.'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'게시글 삭제 중 오류가 발생했습니다: {str(e)}'}), 500
    finally:
        db.close()

