import os
import jinja2
import json

# flask import
from flask import Blueprint, abort, request, current_app, flash, session,\
    g, redirect, url_for, send_from_directory, make_response, jsonify, render_template
from flask.ext.babel import lazy_gettext as _

# project import
from project.utils.auth import not_login_required, login_required, admin_required
from project.utils.template import render, title, ajax_render, smart_render, is_ajax

from . import mod

@mod.route('/profile/', defaults={'username': 'me'})
@mod.route('/profile/<username>/')
@login_required
@title(_('profile'))
def profile(username):
	if username == 'me' or username == g.user.username:
		user = g.user

	return user.username
