# -*- coding: utf-8 -*-


from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.auth import auth
from app.auth.models import User
from app.auth.forms import LoginForm, RegistrationForm
from app import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    form = LoginForm()
    if request.method == 'POST':
        # print '-------------------', request.form.get("username", "")
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None and user.password_hash is not None and user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                flash('You are now logged in. Welcome back!', 'success')
                return redirect(request.args.get('next') or url_for('admin.home'))
            else:
                flash('Invalid username or password.', 'error')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """ Register a new user, and send them a confirmation email."""
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            # confirm_link = url_for('account.confirm', token=token, _external=True)
            # get_queue().enqueue(
            #     send_email,
            #     recipient=user.email,
            #     subject='Confirm Your Account',
            #     template='account/email/confirm',
            #     user=user,
            #     confirm_link=confirm_link)
            # flash('A confirmation link has been sent to {}.'.format(user.email), 'warning')
            flash(u'注册成功.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

