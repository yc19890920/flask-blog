# -*- coding: utf-8 -*-

from flask import url_for
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import BooleanField, PasswordField, StringField, SubmitField, TextAreaField, SelectField, SelectMultipleField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length


class CommentForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(1, 64)])
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    content = TextAreaField(u'内容', validators=[InputRequired()])

class SuggestForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(1, 64)])
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    content = TextAreaField(u'内容', validators=[InputRequired()])
