# -*- coding: utf-8 -*-

import os
basedir = os.path.dirname(os.path.realpath(__file__))


class Config():
    DEBUG = True
    SECRET_KEY = 'secret key to protect from csrf'

    # BASE_DIR
    BASE_DIR = basedir
    CKUPLOAD_URL = "/static/ckupload"
    CKUPLOAD_DIR = os.path.join(BASE_DIR, 'app', "static", "ckupload")


    # 每次request后数据库自动调用commit
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # 连接数据库操作
    SQLALCHEMY_DATABASE_URI = "mysql://fblog:123456@localhost:3306/flaskblog?charset=utf8"
    # SQLALCHEMY_DATABASE_URI = "mysql://fblog:123456@127.0.0.1:3306/flask-blog?charset=utf8"

    UPLOADIMG_HOST = ""


    # 图片路径
    IMG_PATH = 'static/img' # 常规图片存放地方
    AVATAR_IMAGE_PATH = 'static/resource/image/avatar'      # 用户头像路径
    COVER_IMAGE_PATH = 'static/resource/image/cover' # 用户封面图片路径

    ARTICLE_IMAGE_PATH = 'static/resource/image/article' # 文章图片路径

    TMP_PATH = 'static/resource/tmp' # 临时文件目录

    # 页面内容书
    SEARCH_PAGE = 10
    AUTOSEARCH_TOPIC_PAGE = 20
    # HOME_PAGE = 10
    # TOPIC_ARTICLE_PAGE = 10
    # TOPIC_BOOK_PAGE = 15
    USER_PAGE = 10
    USER_TOPIC_PAGE = 20
    # 文章列表页
    ARTICLE_PAGE = 20

    # 预览专题个数
    # 在文章、书籍列表的头部显示的专题个数
    PREVIEW_TOPIC_NUM = 25

    # 搜索配置
    SEARCH_TOPIC_SIZE = 20 # 搜索索引的排行列表

    ARTICLES_PER_PAGE = 10
    COMMENTS_PER_PAGE = 6

    WTF_CSRF_SECRET_KEY = 'random key for form' # for csrf protection
    # Take good care of 'SECRET_KEY' and 'WTF_CSRF_SECRET_KEY', if you use the
    # bootstrap extension to create a form, it is Ok to use 'SECRET_KEY',
    # but when you use tha style like '{{ form.name.labey }}:{{ form.name() }}',
    # you must do this for yourself to use the wtf, more about this, you can
    # take a reference to the book <<Flask Framework Cookbook>>.
    # But the book only have the version of English.

    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    # JWT
    JWT_AUTH_URL_RULE = '/jwt-auth'
    # JWT_AUTH_ENDPOINT = 'jwt'
    # JWT_AUTH_USERNAME_KEY = 'username'
    # JWT_AUTH_PASSWORD_KEY = 'password'

    @staticmethod
    def init_app(app):
        pass
