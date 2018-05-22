# -*- coding: utf-8 -*-

import os
import re
import datetime
from flask import url_for

from app import db, Config
from app.libs.exceptions import ValidationError
from app.libs.tools import smart_bytes

PicP = re.compile(ur'src="(\/static\/ckupload\/.*?)"')

acrticle_tags_ref = db.Table(
    'blog_article_tags',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('blog_tag.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('blog_article.id'))
)

class Tag(db.Model):
    __tablename__ = 'blog_tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False, doc=u"标签名")
    created = db.Column(db.DATETIME, nullable=True, default=datetime.datetime.now(), doc=u"创建时间")
    updated = db.Column(db.DATETIME, nullable=True, default=datetime.datetime.now(), doc=u"修改时间")
    articles = db.relationship('Article', secondary=acrticle_tags_ref, backref=db.backref('tags_articles', lazy='dynamic'))

    def __str__(self):
        return smart_bytes(self.name)

    __repr__ = __str__

    @property
    def get_blog_tag_uri(self):
        return url_for("blog.tag", tag_id=self.id)

    @staticmethod
    def get_choice_lists():
        return [(row.id, row.name) for row in Tag.query.all()]

    @staticmethod
    def str_to_obj(tags):
        r = []
        for tag in tags:
            tag_obj = Tag.query.filter_by(id=int(tag)).first()
            if tag_obj is None:
                continue
            r.append(tag_obj)
        return r

    @property
    def getRefArticleIDs(self):
        return [ d.id for d in self.articles ]


class Category(db.Model):
    __tablename__ = 'blog_category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False, doc=u"分类名")
    created = db.Column(db.DATETIME, nullable=True, default=datetime.datetime.now(), doc=u"创建时间")
    updated = db.Column(db.DATETIME, nullable=True, default=datetime.datetime.now(), doc=u"修改时间")

    def __str__(self):
        return smart_bytes(self.name)

    __repr__ = __str__

    @staticmethod
    def get_choice_lists():
        return [(row.id, row.name) for row in Category.query.all()]

    @staticmethod
    def get_obj(cat_id):
        return Category.query.filter_by(id=int(cat_id)).first()


class Article(db.Model):
    __tablename__ = 'blog_article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, nullable=False, doc=u"标题")
    content = db.Column(db.Text, nullable=False, doc=u"内容")
    abstract = db.Column(db.Text, nullable=False, doc=u"摘要")
    status = db.Column(db.String(1), nullable=False, doc=u"文章状态", default="d")
    views = db.Column(db.Integer, default=0, doc=u'阅读量')
    likes = db.Column(db.Integer, default=0, doc=u'点赞数')
    auth = db.Column(db.String(50), nullable=False, doc=u"作者")
    source = db.Column(db.String(100), nullable=True, doc=u"来源")

    category_id = db.Column(db.Integer, db.ForeignKey('blog_category.id'))
    category = db.relationship('Category', backref=db.backref('category_articles', lazy='dynamic'))

    # 而每个 tag 的页面列表（ Tag.tags_article ）是一个动态的反向引用。 正如上面提到的，这意味着你会得到一个可以发起 select 的查询对象。
    tags = db.relationship('Tag', secondary=acrticle_tags_ref, backref=db.backref('tags_articles', lazy='dynamic'))
    created = db.Column(db.DATETIME, nullable=True, default=datetime.datetime.now(), doc=u"创建时间")
    updated = db.Column(db.DATETIME, nullable=True, default=datetime.datetime.now(), doc=u"修改时间")
    comments = db.relationship('BlogComment', backref='post', lazy='dynamic')

    def __str__(self):
        return smart_bytes(self.title)

    __repr__ = __str__

    @property
    def show_status_display(self):
        if self.status == "p":
            return u"发布"
        return u"延迟发布"

    @property
    def get_modify_uri(self):
        return url_for("admin.article_modify", article_id=self.id)

    @property
    def get_detail_uri(self):
        return url_for("blog.detail", article_id=self.id)

    @property
    def get_tags_id(self):
        return [d.id for d in self.tags]

    @staticmethod
    def referPic(article_id, content, abstract):
        lists = PicP.findall(content)
        lists2 = PicP.findall(abstract)
        l = list( set(lists) | set(lists2) )
        pics = []
        for i in l:
            obj = CKPicture.query.filter_by(filepath=i).first()
            if not obj: continue
            obj.article_id = article_id
            pics.append(obj)
        db.session.add_all(pics)
        db.session.commit()

    @property
    def has_previous_obj(self):
        obj = Article.query.filter_by(status='p').filter(id<self.id).order_by(Article.id.desc()).first()
        return obj and obj.id or None

    @property
    def has_next_obj(self):
        obj = Article.query.filter_by(status='p').filter(id>self.id).order_by(Article.id.asc()).first()
        return obj and obj.id or None

    @property
    def blogcomments(self):
        return BlogComment.query.filter_by(article_id=self.id).order_by(BlogComment.id.desc())

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'title': self.title,
            'content': self.content,
            'abstract': self.abstract,
            'created': self.created,
            'auth': self.auth,
            # 'auth': url_for('api.get_user', id=self.author_id, _external=True),
            'comments': url_for('api.get_post_comments', id=self.id, _external=True),
            'comment_count': self.comments.count()
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        title = json_post.get('title')
        abstract = json_post.get('abstract')
        content = json_post.get('content')
        auth = json_post.get('auth')
        category_id = json_post.get('category_id')
        if title is None or title == '':
            raise ValidationError('post does not have a title')
        if abstract is None or abstract == '':
            raise ValidationError('post does not have a abstract')
        if content is None or content == '':
            raise ValidationError('post does not have a body')
        if auth is None or auth == '':
            raise ValidationError('post does not have a auth')
        if category_id is None or category_id == '':
            raise ValidationError('post does not have a category_id')
        return Article(title=title,abstract=abstract, content=content, auth=auth,category_id=category_id)


# class BlogArticleTasg(db.Model):
#     __tablename__ = 'blog_article_tags'
#
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     tag_id = db.Column(db.Integer, db.ForeignKey('blog_tag.id'))
#     article_id = db.Column(db.Integer, db.ForeignKey('blog_article.id'))

class CKPicture(db.Model):
    __tablename__ = 'blog_picture'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, default=0, index=True) # db.ForeignKey('blog_article.id')
    filename = db.Column(db.String(100), index=True, nullable=False, doc=u"图片名")
    filetype = db.Column(db.String(100), index=True, nullable=False, doc=u"图片类型")
    filepath = db.Column(db.String(200), unique=True, index=True, nullable=False, doc=u"文件路径")
    filesize = db.Column(db.Integer, default=0, doc=u'文件大小')
    created = db.Column(db.DATETIME, nullable=True, default=datetime.datetime.now(), doc=u"创建时间")

    @staticmethod
    def str_to_obj(ids):
        r = []
        for pid in ids:
            tag_obj = CKPicture.query.filter_by(id=int(pid), article_id=0).first()
            if tag_obj is None:
                continue
            r.append(tag_obj)
        return r

    @property
    def refarticle(self):
        obj = Article.query.filter_by(id=self.article_id).first()
        return obj and obj.title or ""

    def removepath(self):
        path = os.path.join(Config.BASE_DIR, self.filepath[1:])
        if os.path.exists(path):
            os.remove( path )


class BlogComment(db.Model):
    __tablename__ = 'blog_comment'

    id = db.Column(db.Integer, primary_key=True)
    # article_id = db.Column(db.Integer, db.ForeignKey('blog_article.id'), default=0, index=True) # db.ForeignKey('blog_article.id')
    article_id = db.Column(db.Integer, db.ForeignKey('blog_article.id'))
    article = db.relationship('Article', backref=db.backref('article_coments', lazy='dynamic'))

    username = db.Column(db.String(100), index=True, nullable=False, doc=u"你的名称")
    email = db.Column(db.String(100), index=True, nullable=False, doc=u"你的邮箱")
    content = db.Column(db.Text, nullable=False, doc=u"评论内容")
    created = db.Column(db.DATETIME, nullable=True, default=datetime.datetime.now(), doc=u"创建时间")
    updated = db.Column(db.DATETIME, nullable=True, default=datetime.datetime.now(), doc=u"修改时间")

    @property
    def refarticle(self):
        obj = Article.query.filter_by(id=self.article_id).first()
        return obj and obj.title or ""

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id),
            'post_url': url_for('api.get_post', id=self.post_id),
            'content': self.content,
            'created': self.created,
            # 'author_url': url_for('api.get_user', id=self.author_id),
        }
        return json_comment

    @staticmethod
    def from_json(json_comment):
        content = json_comment.get('content')
        if content is None or content == '':
            raise ValidationError('comment does not have a body')
        return BlogComment(content=content)


class Suggest(db.Model):
    __tablename__ = 'blog_suggest'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, nullable=False, doc=u"你的名称")
    email = db.Column(db.String(100), index=True, nullable=False, doc=u"你的邮箱")
    content = db.Column(db.Text, nullable=False, doc=u"评论内容")
    created = db.Column(db.DATETIME, nullable=True, default=datetime.datetime.now(), doc=u"创建时间")
