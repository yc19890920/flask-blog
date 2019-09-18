# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_moment import Moment
# from flask_seasurf import SeaSurf

import redis
from settings import Config

db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

redis = redis.Redis(host="127.0.0.1", port=6379, db=0)

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)
db.init_app(app)
from app.api.jwt_auth import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity
jwt = JWT(app, authenticate, identity)

csrf.init_app(app)
bootstrap.init_app(app)
moment.init_app(app)
login_manager.init_app(app)

from app.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from app.admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)

from app.blog import blog as blog_blueprint
app.register_blueprint(blog_blueprint)

from app.api import api as api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/api/v1')

import logging

# rootLogger = logging.getLogger(__name__)
# rootLogger.setLevel(logging.DEBUG)
# socketHandler = logging.handlers.SocketHandler('localhost',logging.handlers.DEFAULT_TCP_LOGGING_PORT)
# rootLogger.addHandler(socketHandler)
# rootLogger.setLevel(logging.DEBUG)
# logger = logging.getLogger(__name__)

@app.before_request
def xxxxxxxxxx1():
    # logger.info('前1')
    print('前1')
    # return "不要再来烦我了"

@app.before_request
def xxxxxxxxxx2():
    # logger.info('前2')
    print('前2')

@app.after_request
def oooooooo1(response):
    # logger.info('后1')
    print('后1')
    return response

@app.after_request
def oooooooo2(response):
    # logger.info('后2')
    print('后2')
    return response

# def create_app():
#     app = Flask(__name__)
#
#     from app.api.jwt_auth import authenticate, identity
#     from flask_jwt import JWT, jwt_required, current_identity
#     jwt = JWT(app, authenticate, identity)
#
#     app.config.from_object(Config)
#     Config.init_app(app)
#     # csrf.init_app(app)
#
#     db.init_app(app)
#     bootstrap.init_app(app)
#     moment.init_app(app)
#     login_manager.init_app(app)
#
#     from app.auth import auth as auth_blueprint
#     app.register_blueprint(auth_blueprint, url_prefix='/auth')
#
#     from app.admin import admin as admin_blueprint
#     app.register_blueprint(admin_blueprint)
#
#     from app.blog import blog as blog_blueprint
#     app.register_blueprint(blog_blueprint)
#
#     from app.api import api as api_blueprint
#     app.register_blueprint(api_blueprint, url_prefix='/api/v1')
#
#     return app