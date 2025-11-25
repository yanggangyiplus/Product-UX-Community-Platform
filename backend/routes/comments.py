"""
댓글 관련 API 라우트
/comments 엔드포인트 포함
"""
from flask import Blueprint, request, jsonify
from database import SessionLocal
from models import Comment, Post
from utils.auth import login_required

comments_bp = Blueprint('comments', __name__, url_prefix='/api/comments')


@comments_bp.route('', methods=['GET'])
def get_comments():
    """댓글 목록 조회"""
    post_id = request.args.get('post_id', type=int)
    
    if not post_id:
        return jsonify({'error': 'post_id가 필요합니다.'}), 400
    
    db = SessionLocal()
    try:
        comments = db.query(Comment).filter(
            Comment.post_id == post_id,
            Comment.is_deleted == False
        ).order_by(Comment.created_at).all()
        
        # 댓글 트리 구조 생성
        comment_dict = {}
        root_comments = []
        
        for comment in comments:
            comment_dict[comment.id] = {
                'id': comment.id,
                'post_id': comment.post_id,
                'author_id': comment.author_id,
                'author_nickname': comment.author.nickname,
                'parent_id': comment.parent_id,
                'content': comment.content,
                'created_at': comment.created_at.isoformat(),
                'updated_at': comment.updated_at.isoformat(),
                'replies': []
            }
        
        for comment in comments:
            if comment.parent_id:
                if comment.parent_id in comment_dict:
                    comment_dict[comment.parent_id]['replies'].append(comment_dict[comment.id])
            else:
                root_comments.append(comment_dict[comment.id])
        
        return jsonify({'comments': root_comments}), 200
    finally:
        db.close()


@comments_bp.route('', methods=['POST'])
@login_required
def create_comment():
    """댓글 작성"""
    data = request.get_json()
    post_id = data.get('post_id')
    content = data.get('content')
    parent_id = data.get('parent_id')
    
    if not post_id or not content:
        return jsonify({'error': 'post_id와 content를 입력해주세요.'}), 400
    
    db = SessionLocal()
    try:
        # 게시글 존재 확인
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return jsonify({'error': '게시글을 찾을 수 없습니다.'}), 404
        
        comment = Comment(
            post_id=post_id,
            author_id=request.current_user_id,
            parent_id=parent_id,
            content=content
        )
        db.add(comment)
        
        # 게시글 댓글 수 증가
        post.comment_count += 1
        
        db.commit()
        
        return jsonify({
            'id': comment.id,
            'message': '댓글이 작성되었습니다.'
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'댓글 작성 중 오류가 발생했습니다: {str(e)}'}), 500
    finally:
        db.close()


@comments_bp.route('/<int:comment_id>', methods=['PUT'])
@login_required
def update_comment(comment_id):
    """댓글 수정"""
    data = request.get_json()
    content = data.get('content')
    
    if not content:
        return jsonify({'error': '내용을 입력해주세요.'}), 400
    
    db = SessionLocal()
    try:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        
        if not comment:
            return jsonify({'error': '댓글을 찾을 수 없습니다.'}), 404
        
        if comment.author_id != request.current_user_id:
            return jsonify({'error': '수정 권한이 없습니다.'}), 403
        
        comment.content = content
        db.commit()
        
        return jsonify({'message': '댓글이 수정되었습니다.'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'댓글 수정 중 오류가 발생했습니다: {str(e)}'}), 500
    finally:
        db.close()


@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    """댓글 삭제 (소프트 삭제)"""
    db = SessionLocal()
    try:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        
        if not comment:
            return jsonify({'error': '댓글을 찾을 수 없습니다.'}), 404
        
        if comment.author_id != request.current_user_id:
            return jsonify({'error': '삭제 권한이 없습니다.'}), 403
        
        comment.is_deleted = True
        
        # 게시글 댓글 수 감소
        post = db.query(Post).filter(Post.id == comment.post_id).first()
        if post:
            post.comment_count = max(0, post.comment_count - 1)
        
        db.commit()
        
        return jsonify({'message': '댓글이 삭제되었습니다.'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'댓글 삭제 중 오류가 발생했습니다: {str(e)}'}), 500
    finally:
        db.close()

