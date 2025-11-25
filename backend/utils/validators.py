"""
입력 검증 스키마
Marshmallow를 사용한 요청 데이터 검증
"""
from marshmallow import Schema, fields, validate, validates, ValidationError


class LoginSchema(Schema):
    """로그인 요청 검증"""
    email = fields.Email(required=True, error_messages={'required': '이메일을 입력해주세요'})
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, error='비밀번호는 최소 6자 이상이어야 합니다'),
        error_messages={'required': '비밀번호를 입력해주세요'}
    )


class RegisterSchema(Schema):
    """회원가입 요청 검증"""
    email = fields.Email(required=True, error_messages={'required': '이메일을 입력해주세요'})
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=100, error='비밀번호는 8~100자 사이여야 합니다'),
        error_messages={'required': '비밀번호를 입력해주세요'}
    )
    nickname = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=50, error='닉네임은 2~50자 사이여야 합니다'),
        error_messages={'required': '닉네임을 입력해주세요'}
    )

    @validates('password')
    def validate_password(self, value):
        """비밀번호 강도 검증"""
        if not any(char.isdigit() for char in value):
            raise ValidationError('비밀번호는 최소 1개의 숫자를 포함해야 합니다')
        if not any(char.isalpha() for char in value):
            raise ValidationError('비밀번호는 최소 1개의 문자를 포함해야 합니다')


class PostCreateSchema(Schema):
    """게시글 작성 요청 검증"""
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=500, error='제목은 1~500자 사이여야 합니다'),
        error_messages={'required': '제목을 입력해주세요'}
    )
    content = fields.Str(
        required=True,
        validate=validate.Length(min=1, error='내용을 입력해주세요'),
        error_messages={'required': '내용을 입력해주세요'}
    )
    category_id = fields.Int(allow_none=True)
    status = fields.Str(
        validate=validate.OneOf(['published', 'draft'], error='상태는 published 또는 draft여야 합니다'),
        missing='published'
    )


class PostUpdateSchema(Schema):
    """게시글 수정 요청 검증"""
    title = fields.Str(validate=validate.Length(min=1, max=500, error='제목은 1~500자 사이여야 합니다'))
    content = fields.Str(validate=validate.Length(min=1, error='내용을 입력해주세요'))
    category_id = fields.Int(allow_none=True)
    status = fields.Str(
        validate=validate.OneOf(['published', 'draft', 'deleted'], error='유효하지 않은 상태입니다')
    )


class CommentCreateSchema(Schema):
    """댓글 작성 요청 검증"""
    content = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=1000, error='댓글은 1~1000자 사이여야 합니다'),
        error_messages={'required': '댓글 내용을 입력해주세요'}
    )
    parent_id = fields.Int(allow_none=True)


class ReportCreateSchema(Schema):
    """신고 생성 요청 검증"""
    report_type = fields.Str(
        required=True,
        validate=validate.OneOf(['post', 'comment'], error='신고 유형은 post 또는 comment여야 합니다'),
        error_messages={'required': '신고 유형을 선택해주세요'}
    )
    target_id = fields.Int(
        required=True,
        error_messages={'required': '신고 대상 ID를 입력해주세요'}
    )
    reason = fields.Str(
        required=True,
        validate=validate.Length(min=10, max=500, error='신고 사유는 10~500자 사이여야 합니다'),
        error_messages={'required': '신고 사유를 입력해주세요'}
    )


class CategoryCreateSchema(Schema):
    """카테고리 생성 요청 검증"""
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100, error='카테고리명은 1~100자 사이여야 합니다'),
        error_messages={'required': '카테고리명을 입력해주세요'}
    )
    description = fields.Str(allow_none=True)
    order = fields.Int(missing=0)


def validate_request(schema_class):
    """요청 데이터 검증 데코레이터"""
    from functools import wraps
    from flask import request, jsonify

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            schema = schema_class()
            try:
                data = request.get_json()
                errors = schema.validate(data)
                if errors:
                    return jsonify({'error': '입력값이 올바르지 않습니다', 'details': errors}), 400
                # 검증된 데이터를 request에 추가
                request.validated_data = schema.load(data)
            except Exception as e:
                return jsonify({'error': '잘못된 요청 형식입니다', 'details': str(e)}), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator
