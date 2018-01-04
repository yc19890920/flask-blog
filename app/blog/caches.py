# -*- coding: utf-8 -*-

import json
from app import redis
from app.blog.models import Tag, Article, BlogComment

REDIS_KEY = "flask:cce7e4f11fc518f7fff230079ab0edc9"

# 标签缓存
def getTaglist():
    key = "{}:tag".format(REDIS_KEY)
    field = "tag"
    if redis.exists(key):
        vals = json.loads( redis.hget(key, field) )
    else:
        vals = []
        lists = Tag.query.order_by(Tag.name).all()
        for d in lists:
            vals.append( { "id": d.id, "name": d.name } )
        if vals:
            p = redis.pipeline()
            p.hset(key, field, json.dumps(vals))
            p.expire(key, 60*60)
            p.execute()
    return vals

# 最热文章列表
def getHotlist():
    key = "{}:article:hot".format(REDIS_KEY)
    field = "hot"
    if redis.exists(key):
        vals = json.loads( redis.hget(key, field) )
    else:
        vals = []
        lists = Article.query.filter_by(status='p').order_by(Article.views.desc()).limit(10)
        for d in lists:
            vals.append( { "id": d.id, "title": d.title } )
        if vals:
            p = redis.pipeline()
            p.hset(key, field, json.dumps(vals))
            p.expire(key, 15*60)
            p.execute()
    return vals


# 最新文章列表
def getNewArticlelist():
    key = "{}:article:new".format(REDIS_KEY)
    field = "new"
    if redis.exists(key):
        vals = json.loads( redis.hget(key, field) )
    else:
        vals = []
        lists = Article.query.filter_by(status='p').order_by(Article.id.desc()).limit(10)
        for d in lists:
            vals.append( { "id": d.id, "title": d.title } )
        if vals:
            p = redis.pipeline()
            p.hset(key, field, json.dumps(vals))
            p.expire(key, 15*60)
            p.execute()
    return vals


# 最新评论
def getNewCommontlist():
    key = "{}:comment:new".format(REDIS_KEY)
    field = "new"
    if redis.exists(key):
        vals = json.loads( redis.hget(key, field) )
    else:
        vals = []
        lists = BlogComment.query.order_by(BlogComment.id.desc()).limit(10).all()
        for d in lists:
            vals.append( { "id": d.id, "article_id": d.article_id, "content": d.content } )
        if vals:
            p = redis.pipeline()
            p.hset(key, field, json.dumps(vals))
            p.expire(key, 15*60)
            p.execute()
    return vals


# 文章点击 缓存
def shouldIncrViews(ip, article_id):
    key = "{}:{}:{}:article:view".format(REDIS_KEY, ip, article_id)
    if redis.exists(key):
        return False
    p = redis.pipeline()
    p.set(key, "1")
    p.expire(key, 5*60)
    p.execute()
    return True


def getLinks(ip, article_id):
    key = "{}:{}:{}:article:links".format(REDIS_KEY, ip, article_id)
    if redis.exists(key):
        return False
    return True


