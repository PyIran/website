# flask import
from flask import Blueprint, abort, request, current_app, session,\
    g, redirect, url_for, send_from_directory, make_response, jsonify, flash
from flask.ext.babel import lazy_gettext as _
from werkzeug.security import check_password_hash, generate_password_hash


# project import
from project.utils.auth import not_login_required, login_required, admin_required, roles_accepted
from project.utils.template import render, title, ajax_render, smart_render, is_ajax
from project.apps.user.forms import LoginForm
from project.apps.user.models import * 
from project.database import db_session
from . import mod

@mod.route('/')
@login_required
def userindex():
     try:
        return 'You are loggined as ' + g.user.username 
     except:
        return redirect(url_for('user.login'))

@mod.route('/login/', methods=['GET', 'POST'])
#@not_login_required
@title(_('login'))
def login():
    """
    """
    if request.method != 'POST':
        form = LoginForm()
        return render('user/login.html', login_form=form) 

    next = request.args.get('next', None)
    form = LoginForm(request.form)
    form.validate()

    username = form.data['username']
    password = form.data['password']
    if username != '':
        try:
            user = Profile.query.filter(Profile.username == username).first()
        except:
            current_app.logger.warning(
                'login user not found %s' %
                form.data[
                    'username'])
            flash(_("User and password not match!"), "danger")
            return render('user/login.html', login_form=form)
    try:
        if not check_password_hash(user.password, password):
            current_app.logger.warning(
                'login user and password not match %s - %s ' %
                (form.data['username'], form.data['password']))
            flash(_("User and password not match!"), "danger")
            return render('user/login.html', login_form=form)
    except:
            flash(_("User and password not match!"), "danger")
            return render('user/login.html', login_form=form)

    current_app.logger.debug('user %s loggined' % form.data['username'])
    session['username'] = username
    if next:
        return redirect(next)
    return redirect(url_for('user.profile', user=user))
    
@mod.route('/logout/')
@login_required
@title(_('logout'))
def logout():
    """
    """
    current_app.logger.debug('user %s logouted' % g.user.username)
    del(session['username'])
    return redirect(url_for('main.index'))
    