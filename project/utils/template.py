import json
import uuid
from functools import wraps
import datetime

from flask import g, current_app, render_template, g, jsonify, redirect, request, Response, make_response
from flask.ext.babel import lazy_gettext as _

from project.apps.user.models import Log
from project.database import db_session

def title(title=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = '-1'
            try:
                user = g.user.id
            except:
                pass
            log = Log(
                log_date = str(datetime.datetime.now()), 
                log_desc = _('go to :') + title,
                log_user = user
            )
            session = db_session()
            session._model_changes = {}
            session.add(log)
            session.commit()

            g.page_title = title
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def base_path():
    """
    return true path to template
    """
    return ""

def path(addr):
    """
    dar in function address template sakhte mishavad
    """
    if addr.startswith("."):
        template_full = addr[1:]
    else:
        template_full = base_path() + "/" + addr

    return template_full


def render(template, **context):
    return render_template(path(template), **context)


def ajax_render(template, **context):
    if template.endswith('form.html'):
        template = template.replace('form.html', 'base_form.html')
    return jsonify(html=render(template, **context))


def ajax_redirect(url):
    return jsonify(redirect=redirect(url))


def is_ajax():
    """
    """
    return request.headers.get('X_REQUESTED_WITH') == 'XMLHttpRequest'


def smart_render(template, **context):
    """
    """
    if is_ajax():
        return ajax_render(template, **context)
    else:
        return render(template, **context)


def smart_render_with_opt(template, **context):
    """
    """
    if is_ajax():
        return ajax_render(template['ajax'], **context)
    else:
        return render(template['simple'], **context)


def render_ajax_or_redirect(path, template, **context):
    if is_ajax():
        return ajax_render(template['ajax'], **context)
    else:
        return redirect(path)


def render_dict_as_json(data):
    return Response(json.dumps(data), mimetype='application/json')


def unicode_jsonify(data):
    # try:
    #     resp = make_response(json.dumps(data, indent=2, ensure_ascii=False))
    # except:
    resp = make_response(json.dumps(data, indent=2))
    resp.headers['Content-Type'] = "text/html; charset=utf-8"
    return resp


def flash(msg):
    return render('base/flash.html', msg=msg)


def render_table(title, data):
    data['id'] = str(uuid.uuid4())
    data['title'] = title
    return render('table.html', **data)
