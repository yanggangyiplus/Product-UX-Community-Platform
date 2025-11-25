"""
신고 관련 API 라우트
/reports 엔드포인트 포함
"""
from flask import Blueprint, request, jsonify
from database import SessionLocal
from models import Report, ReportType, ReportStatus, Post, Comment
from utils.auth import login_required

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')


@reports_bp.route('', methods=['POST'])
@login_required
def create_report():
    """신고 생성"""
    data = request.get_json()
    report_type = data.get('report_type')
    post_id = data.get('post_id')
    comment_id = data.get('comment_id')
    reason = data.get('reason')
    
    if not report_type or not reason:
        return jsonify({'error': '신고 유형과 사유를 입력해주세요.'}), 400
    
    if report_type not in ['post', 'comment']:
        return jsonify({'error': '잘못된 신고 유형입니다.'}), 400
    
    if report_type == 'post' and not post_id:
        return jsonify({'error': 'post_id가 필요합니다.'}), 400
    
    if report_type == 'comment' and not comment_id:
        return jsonify({'error': 'comment_id가 필요합니다.'}), 400
    
    db = SessionLocal()
    try:
        # 중복 신고 확인
        existing_report = db.query(Report).filter(
            Report.reporter_id == request.current_user_id,
            Report.report_type == ReportType[report_type.upper()],
            Report.post_id == post_id if report_type == 'post' else None,
            Report.comment_id == comment_id if report_type == 'comment' else None,
            Report.status == ReportStatus.PENDING
        ).first()
        
        if existing_report:
            return jsonify({'error': '이미 신고한 항목입니다.'}), 400
        
        # 대상 존재 확인
        if report_type == 'post':
            post = db.query(Post).filter(Post.id == post_id).first()
            if not post:
                return jsonify({'error': '게시글을 찾을 수 없습니다.'}), 404
        
        if report_type == 'comment':
            comment = db.query(Comment).filter(Comment.id == comment_id).first()
            if not comment:
                return jsonify({'error': '댓글을 찾을 수 없습니다.'}), 404
        
        report = Report(
            reporter_id=request.current_user_id,
            report_type=ReportType[report_type.upper()],
            post_id=post_id,
            comment_id=comment_id,
            reason=reason,
            status=ReportStatus.PENDING
        )
        db.add(report)
        db.commit()
        
        return jsonify({
            'id': report.id,
            'message': '신고가 접수되었습니다.'
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'신고 처리 중 오류가 발생했습니다: {str(e)}'}), 500
    finally:
        db.close()


@reports_bp.route('', methods=['GET'])
@login_required
def get_reports():
    """신고 목록 조회 (관리자용)"""
    # 관리자 권한 확인은 admin 라우트에서 처리
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
                'created_at': report.created_at.isoformat()
            } for report in reports],
            'total': total,
            'page': page,
            'per_page': per_page
        }), 200
    finally:
        db.close()

