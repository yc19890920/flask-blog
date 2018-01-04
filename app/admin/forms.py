# -*- coding: utf-8 -*-

from flask import url_for
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import BooleanField, PasswordField, StringField, SubmitField, TextAreaField, SelectField, SelectMultipleField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from app.blog.models import Article, Category

ARTICLE_STATUS = [('p', u'发布'), ('d', u'延迟发布')]

class ArticleForm(FlaskForm):
    title = StringField(u'标题', validators=[InputRequired(), Length(1, 100)])
    content = TextAreaField(u'内容', validators=[InputRequired()])
    abstract = TextAreaField(u'摘要', validators=[InputRequired()])
    auth = StringField(u'作者', validators=[InputRequired(), Length(1, 50)])
    source = StringField(u'来源')
    status = SelectField(u"文章状态", validators=[InputRequired()], choices=ARTICLE_STATUS)
    category = SelectField(u"分类", coerce=int, validators=[InputRequired()])
    tags = SelectMultipleField(u"标签", coerce=int, validators=[InputRequired()])