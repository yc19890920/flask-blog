# -*- coding: utf-8 -*-
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from app.auth.models import User
from . import api

# JWT鉴权：默认参数为username/password，在数据库里查找并比较password_hash
def authenticate(username, password):
    print 'JWT auth argvs:', username, password
    user = User.query.filter_by(username=username).first()
    if user is not None and user.verify_password(password):
        return user

# JWT检查user_id是否存在
def identity(payload):
    print 'JWT payload:', payload
    user_id = payload['identity']
    user = User.query.filter_by(id=user_id).first()
    return user_id if user is not None else None




