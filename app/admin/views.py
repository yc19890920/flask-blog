# -*- coding: utf-8 -*-

import os
import re
import json
import uuid
import random
from flask import Response, make_response
from flask_login import login_required
from flask import flash, redirect, render_template, request, url_for, abort
from jinja2.nativetypes import NativeEnvironment

from app import db, csrf, Config
from app.admin import admin
from app.admin.forms import ArticleForm
from app.blog.models import Tag, Category, Article, CKPicture, BlogComment, Suggest


############################################
@admin.route('/admin/home', methods=['GET'])
@login_required
def home():
    return render_template('admin/home.html')


############################################
@admin.route('/admin/tag', methods=['GET', 'POST'])
@login_required
def tag():
    if request.method == "POST":
        id = request.form.get('id', "")
        name = request.form.get('name', "").strip()
        status = request.form.get('status', "")
        if status == "delete":
            obj = Tag.query.filter_by(id=id).first()
            db.session.delete(obj)
            db.session.commit()
            flash(u'删除成功', 'success')
        if status == "add":
            if not name:
                flash(u'输入为空，操作失败', 'error')
                return redirect(url_for('admin.tag'))
            if Tag.query.filter_by(name=name).first():
                flash(u'重复添加，添加失败', 'error')
            else:
                tag = Tag(name=name)
                db.session.add(tag)
                db.session.commit()
                flash(u'添加成功', 'success')
        return redirect(url_for('admin.tag'))

    tag_list = Tag.query.all()
    return render_template('admin/blog/tag.html', tag_list=tag_list)


############################################
@admin.route('/admin/category', methods=['GET', 'POST'])
@login_required
def category():
    if request.method == "POST":
        id = request.form.get('id', "")
        name = request.form.get('name', "").strip()
        status = request.form.get('status', "")
        if status == "delete":
            obj = Category.query.filter_by(id=id).first()
            db.session.delete(obj)
            db.session.commit()
            flash(u'删除成功', 'success')
        if status == "add":
            if not name:
                flash(u'输入为空，操作失败', 'error')
                return redirect(url_for('admin.category'))
            if Category.query.filter_by(name=name).first():
                flash(u'重复添加，添加失败', 'error')
            else:
                tag = Category(name=name)
                db.session.add(tag)
                db.session.commit()
                flash(u'添加成功', 'success')
        return redirect(url_for('admin.category'))

    tag_list = Category.query.all()
    return render_template('admin/blog/category.html', tag_list=tag_list)

############################################
@admin.route('/admin/article', methods=['GET', 'POST'])
@login_required
def article():
    if request.method == "POST":
        id = request.form.get('id', "")
        status = request.form.get('status', "")
        if status == "delete":
            obj = Article.query.filter_by(id=id).first()
            if obj:
                Article.referPic(0, obj.content, obj.abstract)
                db.session.delete(obj)
                db.session.commit()
            flash(u'删除成功', 'success')
        return redirect(url_for('admin.article'))
    return render_template('admin/blog/article.html')


@admin.route('/admin/article/ajax', methods=['GET', 'POST'])
@login_required
def article_ajax():
    data = request.args
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'title']

    order_T = Article.id.desc()
    if order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            if int(order_column) == 0:
                order_T = Article.id.desc()
            else:
                order_T = Article.title.desc()
        else:
            if int(order_column) == 0:
                order_T = Article.id.asc()
            else:
                order_T = Article.title.asc()

    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1

    try:
        start_num = int(data.get('start', '0'))
        page = start_num / length + 1
    except ValueError:
        start_num = 0
        page = 1

    count = Article.query.count()
    if start_num >= count:
        page = 1

    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    # if search:
    #     pagination = Article.query.filter(Article.title.like("%%s%", search)).order_by(order_T).paginate(page, per_page=length, error_out = False)
    # else:
    #     pass
    pagination = Article.query.order_by(order_T).paginate(page, per_page=length, error_out = False)
    lists = pagination.items
    number = length * (page-1) + 1

    for d in lists:
        html = render_template('admin/blog/ajax_article.html', d=d, number=number)
        rs["aaData"].append(re.findall(re_str, html, re.DOTALL))
        number += 1
    return Response(json.dumps(rs), content_type="application/json")


    env = NativeEnvironment()
    from_string = u"""
        <td>{{ number }}</td>
        <td>{{ d.title|e }}</td>
        <td>{{ d.show_status_display }}</td>
        <td>{{ d.auth|e }}</td>
        <td>{{ d.source|e }}</td>
        <td>{{ d.views }}</td>
        <td>{{ d.likes }}</td>
        <td>{{ d.created }}</td>
        <td>{{ d.updated }}</td>
        <td>{{ d.category.name }}</td>
        <td>
            {% for t in d.tags %}
                <button type="button" class="btn btn-minier btn-primary "> {{ t.name }}</button>
            {% endfor %}
        </td>
        <td>
            <a type="button" class="btn btn-minier btn-primary" href="{{ d.get_modify_uri }}">修改</a>
            <a type="button" class="btn btn-minier btn-danger" href="Javascript: setStatus({{ d.id }}, 'delete')">删除</a>
            {% if d.status == 'p' %}
                <a class="btn btn-minier btn-primary" href="#" target="_blank">查看文章</a>
            {% endif %}
        </td>
    """
    for d in lists:
        t = env.from_string(from_string)
        result = t.render(number=number, d=d)
        rs["aaData"].append(re.findall(re_str, result, re.DOTALL))
        number += 1
    return Response(json.dumps(rs), content_type="application/json")


@admin.route('/admin/article/add', methods=['GET', 'POST'])
@login_required
def article_add():
    if request.method == "POST":
        form = ArticleForm(request.form)
        form.category.choices = Category.get_choice_lists()
        form.tags.choices = Tag.get_choice_lists()
        # if form.validate_on_submit():
        if form.validate():
            article = Article(
                title=form.title.data, content=form.content.data, abstract=form.abstract.data,
                auth=form.auth.data, source=form.source.data, status=form.status.data,
                category=Category.get_obj(int(form.category.data)), tags=Tag.str_to_obj(form.tags.data))
            db.session.add(article)
            db.session.commit()
            Article.referPic(article.id, form.content.data, form.abstract.data)

            flash(u'添加文章成功.', 'success')
            return redirect(url_for('admin.article'))
    else:
        form = ArticleForm(title="", content="", abstract="", auth="Y.c", source="", status="p", category_id=0, tags=[2,])
        form.category.choices = Category.get_choice_lists()
        form.tags.choices = Tag.get_choice_lists()
    return render_template('admin/blog/article_add.html', form=form)

@admin.route('/admin/article/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def article_modify(article_id):
    article_obj = Article.query.filter_by(id=article_id).first_or_404()
    # article_obj = Article.query.get(article_id)
    # if article_obj is None:
    #     abort(404)
    if request.method == "POST":
        form = ArticleForm(request.form)
        form.category.choices = Category.get_choice_lists()
        form.tags.choices = Tag.get_choice_lists()
        if form.validate():
            article_obj.title = form.title.data
            article_obj.content = form.content.data
            article_obj.abstract = form.abstract.data
            article_obj.auth = form.auth.data
            article_obj.source = form.source.data
            article_obj.status = form.status.data
            article_obj.Category = Category.get_obj(int(form.category.data))
            article_obj.tags = Tag.str_to_obj(form.tags.data)

            Article.referPic(0, form.content.data, form.abstract.data)
            db.session.add(article_obj)
            db.session.commit()
            Article.referPic(article_id, form.content.data, form.abstract.data)

            flash(u'修改文章成功.', 'success')
            return redirect(url_for('admin.article'))
    else:
        form = ArticleForm(
            title=article_obj.title, content=article_obj.content, abstract=article_obj.abstract,
            auth=article_obj.auth, source=article_obj.source, status=article_obj.status,
            category=article_obj.category_id, tags=article_obj.get_tags_id
        )
        form.category.choices = Category.get_choice_lists()
        form.tags.choices = Tag.get_choice_lists()
    return render_template('admin/blog/article_add.html', form=form)

@csrf.exempt
@admin.route('/admin/ckupload', methods=['POST'])
@login_required
def ckupload():
    """CKEditor file upload"""
    error = ''
    callback = request.args.get("CKEditorFuncNum")
    print request.files['upload']
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        content_type = fileobj.content_type
        size = fileobj.content_length
        fname = fileobj.filename
        fext = os.path.splitext(fname)[-1]
        uuname = '{}{}{}'.format(str(uuid.uuid1()).replace("-", ""), random.randint(1, 100000), fext)
        url = url_for('static', filename='%s/%s' % ('ckupload', uuname))
        try:
            fname = fname.encode("utf-8")
        except BaseException as e:
            fname = uuname
            print e
        path = os.path.join(Config.CKUPLOAD_DIR, uuname)
        fileobj.save(path)

        ck = CKPicture( filename=fname, filetype=content_type, filepath=url,filesize=size )
        db.session.add(ck)
        db.session.commit()

        res = """
        <script type="text/javascript">
          window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
        </script>
        """ % (callback, url, error)
        response = make_response(res)
        response.headers["Content-Type"] = "text/html"
        return response
    raise abort(403)

############################################
@admin.route('/admin/picture', methods=['GET', 'POST'])
@login_required
def picture():
    if request.method == "POST":
        status = request.form.get('status', "")
        if status == "delete":
            id = request.form.get('id', "")
            obj = CKPicture.query.filter_by(id=int(id), article_id=0).first()
            if obj:
                obj.removepath()
                db.session.delete(obj)
                db.session.commit()
            flash(u'删除成功', 'success')
        if status == "deleteall":
            ids = ( request.form.get('ids', False) ).split(',')
            objs = CKPicture.str_to_obj(ids)
            for obj in objs:
                obj.removepath()
                db.session.delete(obj)
            db.session.commit()
            flash(u'批量删除成功', 'success')
        return redirect(url_for('admin.picture'))
    tag_list = CKPicture.query.all()
    return render_template('admin/blog/picture.html', tag_list=tag_list)

############################################
@admin.route('/admin/comment', methods=['GET', 'POST'])
@login_required
def comment():
    if request.method == "POST":
        id = request.form.get('id', "")
        status = request.form.get('status', "")
        if status == "delete":
            obj = BlogComment.query.filter_by(id=id).first()
            if obj:
                db.session.delete(obj)
                db.session.commit()
            flash(u'删除成功', 'success')
        return redirect(url_for('admin.comment'))
    tag_list = BlogComment.query.all()
    return render_template('admin/blog/comment.html', tag_list=tag_list)

############################################
@admin.route('/admin/suggest', methods=['GET', 'POST'])
@login_required
def suggest():
    if request.method == "POST":
        id = request.form.get('id', "")
        status = request.form.get('status', "")
        if status == "delete":
            obj = Suggest.query.filter_by(id=id).first()
            if obj:
                db.session.delete(obj)
                db.session.commit()
            flash(u'删除成功', 'success')
        return redirect(url_for('admin.suggest'))
    tag_list = Suggest.query.all()
    return render_template('admin/blog/suggest.html', tag_list=tag_list)

