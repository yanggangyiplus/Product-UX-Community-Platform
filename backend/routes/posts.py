"""
게시글 관련 API 라우트
/posts 엔드포인트 포함
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import SessionLocal
from models import Post, PostImage, PostLike, PostStatus, Category
from sqlalchemy import desc
from utils.auth import login_required

posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')


@posts_bp.route('', methods=['GET'])
def get_posts():
    """게시글 목록 조회"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', '')
    
    db = SessionLocal()
    try:
        query = db.query(Post).filter(Post.status == PostStatus.PUBLISHED)
        
        if category_id:
            query = query.filter(Post.category_id == category_id)
        
        if search:
            query = query.filter(
                Post.title.contains(search) | Post.content.contains(search)
            )
        
        posts = query.order_by(desc(Post.created_at)).offset((page - 1) * per_page).limit(per_page).all()
        total = query.count()
        
        return jsonify({
            'posts': [{
                'id': post.id,
                'title': post.title,
                'content': post.content[:200],  # 미리보기
                'author_id': post.author_id,
                'author_nickname': post.author.nickname,
                'category_id': post.category_id,
                'category_name': post.category.name if post.category else None,
                'view_count': post.view_count,
                'like_count': post.like_count,
                'comment_count': post.comment_count,
                'created_at': post.created_at.isoformat(),
                'updated_at': post.updated_at.isoformat()
            } for post in posts],
            'total': total,
            'page': page,
            'per_page': per_page
        }), 200
    finally:
        db.close()


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """게시글 상세 조회"""
    db = SessionLocal()
    try:
        post = db.query(Post).filter(
            Post.id == post_id,
            Post.status == PostStatus.PUBLISHED
        ).first()
        
        if not post:
            return jsonify({'error': '게시글을 찾을 수 없습니다.'}), 404
        
        # 조회수 증가
        post.view_count += 1
        db.commit()
        
        return jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author_id': post.author_id,
            'author_nickname': post.author.nickname,
            'category_id': post.category_id,
            'category_name': post.category.name if post.category else None,
            'view_count': post.view_count,
            'like_count': post.like_count,
            'comment_count': post.comment_count,
            'images': [img.image_url for img in sorted(post.images, key=lambda x: x.order)],
            'created_at': post.created_at.isoformat(),
            'updated_at': post.updated_at.isoformat()
        }), 200
    finally:
        db.close()


@posts_bp.route('', methods=['POST'])
@login_required
def create_post():
    """게시글 작성"""
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    category_id = data.get('category_id')
    images = data.get('images', [])
    status = data.get('status', 'published')
    
    if not title or not content:
        return jsonify({'error': '제목과 내용을 입력해주세요.'}), 400
    
    db = SessionLocal()
    try:
        post_status = PostStatus.PUBLISHED if status == 'published' else PostStatus.DRAFT
        
        post = Post(
            author_id=request.current_user_id,
            category_id=category_id,
            title=title,
            content=content,
            status=post_status
        )
        db.add(post)
        db.flush()
        
        # 이미지 추가
        for idx, image_url in enumerate(images):
            post_image = PostImage(
                post_id=post.id,
                image_url=image_url,
                order=idx
            )
            db.add(post_image)
        
        db.commit()
        
        return jsonify({
            'id': post.id,
            'message': '게시글이 작성되었습니다.'
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'게시글 작성 중 오류가 발생했습니다: {str(e)}'}), 500
    finally:
        db.close()


@posts_bp.route('/<int:post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    """게시글 수정"""
    data = request.get_json()
    
    db = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        
        if not post:
            return jsonify({'error': '게시글을 찾을 수 없습니다.'}), 404
        
        if post.author_id != request.current_user_id:
            return jsonify({'error': '수정 권한이 없습니다.'}), 403
        
        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
            post.content = data['content']
        if 'category_id' in data:
            post.category_id = data['category_id']
        if 'status' in data:
            post.status = PostStatus.PUBLISHED if data['status'] == 'published' else PostStatus.DRAFT
        
        db.commit()
        
        return jsonify({'message': '게시글이 수정되었습니다.'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'게시글 수정 중 오류가 발생했습니다: {str(e)}'}), 500
    finally:
        db.close()


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    """게시글 삭제"""
    db = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        
        if not post:
            return jsonify({'error': '게시글을 찾을 수 없습니다.'}), 404
        
        if post.author_id != request.current_user_id:
            return jsonify({'error': '삭제 권한이 없습니다.'}), 403
        
        post.status = PostStatus.DELETED
        db.commit()
        
        return jsonify({'message': '게시글이 삭제되었습니다.'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'게시글 삭제 중 오류가 발생했습니다: {str(e)}'}), 500
    finally:
        db.close()


@posts_bp.route('/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    """게시글 좋아요"""
    db = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        
        if not post:
            return jsonify({'error': '게시글을 찾을 수 없습니다.'}), 404
        
        # 이미 좋아요 했는지 확인
        existing_like = db.query(PostLike).filter(
            PostLike.user_id == request.current_user_id,
            PostLike.post_id == post_id
        ).first()
        
        if existing_like:
            # 좋아요 취소
            db.delete(existing_like)
            post.like_count = max(0, post.like_count - 1)
            message = '좋아요가 취소되었습니다.'
        else:
            # 좋아요 추가
            new_like = PostLike(
                user_id=request.current_user_id,
                post_id=post_id
            )
            db.add(new_like)
            post.like_count += 1
            message = '좋아요가 추가되었습니다.'
        
        db.commit()
        
        return jsonify({
            'message': message,
            'like_count': post.like_count
        }), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'좋아요 처리 중 오류가 발생했습니다: {str(e)}'}), 500
    finally:
        db.close()

