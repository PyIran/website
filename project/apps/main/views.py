#-*- coding: utf-8 -*-
import re
import urllib2
import simplejson
import datetime

# flask import
from flask import Blueprint, abort, request, current_app, flash, session, g, \
		redirect, url_for, send_from_directory, make_response, jsonify, render_template, json
from flask.ext.babel import lazy_gettext as _
from sqlalchemy import desc

#project import
from project.utils.appconf import noindex
from project.utils.auth import login_required

mod = Blueprint('main', __name__, url_prefix='/')

@mod.route('/')
@noindex
def index():
	return render_template("index.html")

