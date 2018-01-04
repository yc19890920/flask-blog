# -*- coding: utf-8 -*-

import json
from flask import Response
from flask import flash, redirect, render_template, request, url_for, abort

from app import db, csrf
from app.blog import blog, caches
from app.blog.forms import CommentForm, SuggestForm
from app.blog.models import Tag, Article, BlogComment, Suggest
from app.libs import tools

@blog.route('/', methods=['GET'])
def index():
    length = 5
    page = request.args.get('page', '1')
    page = page and int(page) or 1
    pagination = Article.query.filter_by(status='p').paginate(page, per_page=length, error_out = False)

    tag_list = caches.getTaglist()
    hot_list = caches.getHotlist()
    newart_list = caches.getNewArticlelist()
    newcom_list = caches.getNewCommontlist()

    return render_template(
        'blog/index.html',
        article_list=pagination,

        tag_list = tag_list,
        hot_list = hot_list,
        newart_list = newart_list,
        newcom_list = newcom_list,
    )

@blog.route('/p/<int:article_id>/', methods=['GET', "POST"])
def detail(article_id):
    article = Article.query.get_or_404(article_id)
    form = CommentForm()
    if request.method == "POST":
        if form.validate():
            obj = BlogComment(
                username=form.username.data,
                email=form.email.data,
                content=form.content.data,
                article=article
            )
            db.session.add(obj)
            db.session.commit()
            flash(u'您宝贵的意见已收到，谢谢！.', 'success')
            current_uri = "{}#list-talk".format( url_for('blog.detail', article_id=article_id) )
            return redirect(current_uri)

    tag_list = caches.getTaglist()
    hot_list = caches.getHotlist()
    newart_list = caches.getNewArticlelist()

    # 相关文章
    # refer_list = article.get_refer_articles()
    ip = tools.getClientIP()
    if caches.shouldIncrViews(ip, article_id):
        article.views += 1
        db.session.add(article)
        db.session.commit()

    return render_template(
        'blog/detail.html',
        article=article,
        form=form,

        tag_list = tag_list,
        hot_list = hot_list,
        newart_list = newart_list,
    )

@csrf.exempt
@blog.route('/s/', methods=['POST'])
def score():
    if request.method == "POST":
        article_id = request.form.get("poid", "0")
        article = Article.query.get_or_404(article_id)
        article.likes += 1
        db.session.add(article)
        db.session.commit()
    return Response(json.dumps({'status': "ok"}), content_type="application/json")

@blog.route('/q/', methods=['GET'])
def search():
    search_for = request.args.get('search_for')
    if search_for:
        length = 5
        page = request.args.get('page', '1')
        page = page and int(page) or 1
        article_list = Article.query.filter_by(status='p').filter(Article.title.like(search_for)).paginate(page, per_page=length, error_out = False)

        tag_list = caches.getTaglist()
        hot_list = caches.getHotlist()
        newart_list = caches.getNewArticlelist()
        newcom_list = caches.getNewCommontlist()
        return render_template(
            'blog/index.html',
            search_for=search_for,
            article_list=article_list,

            tag_list = tag_list,
            hot_list = hot_list,
            newart_list = newart_list,
            newcom_list = newcom_list,
        )
    return redirect(url_for('blog.index'))

@blog.route('/t/<int:tag_id>/', methods=['GET'])
def tag(tag_id):
    length = 5
    page = request.args.get('page', '1')
    page = page and int(page) or 1
    tag_obj = Tag.query.get_or_404(tag_id)
    article_list = Article.query.filter_by(status='p').filter(
        Article.id.in_(tag_obj.getRefArticleIDs)
    ).paginate(
        page, per_page=length, error_out = False)

    tag_list = caches.getTaglist()
    hot_list = caches.getHotlist()
    newart_list = caches.getNewArticlelist()
    newcom_list = caches.getNewCommontlist()
    return render_template(
        'blog/index.html',
        tag_name=tag_obj,
        article_list=article_list,

        tag_list = tag_list,
        hot_list = hot_list,
        newart_list = newart_list,
        newcom_list = newcom_list,
    )

@blog.route('/about', methods=['GET', 'POST'])
def about():
    form = SuggestForm()
    if request.method == "POST":
        if form.validate():
            obj = Suggest(
                username=form.username.data,
                email=form.email.data,
                content=form.content.data
            )
            db.session.add(obj)
            db.session.commit()
            flash(u'您宝贵的意见已收到，谢谢！.', 'success')
            return redirect(url_for('blog.about'))
    return render_template('blog/about.html', form=form)

