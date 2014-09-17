from functools import wraps
from flask import g, request, redirect, url_for, abort

from .template import is_ajax


def _get_unauthorized_view():
    if g.user.has_group('guest'):
        if is_ajax():
            return abort(403)
        return redirect(url_for('user.login', next=request.url))
    abort(403)


def roles_accepted(*roles):
    """Decorator which specifies that a user must have at least one of the
    specified roles. Example::

        @app.route('/account')
        @roles_accepted('accounter', 'admin')
        def accounter():
            return 'accounter'

    The current user must have either the `accounter` role or `admin` role in
    order to view the page.

    :param args: The possible roles.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if g.user.can(roles):
                return fn(*args, **kwargs)
            return _get_unauthorized_view()
        return decorated_view
    return wrapper


def not_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user.has_group('guest'):
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


login_required = roles_accepted('login')
admin_required = roles_accepted('admin', 'pyiran')

class GuestUser(object):

    """
    """
    username = 'guest'
    group_list = 'guest'
    showable_name = 'guest'

    def can(self, roles):
        if 'guest' in roles:
            return True
        return False

    def has_group(self, group):
        """
        """
        if group == 'guest':
            return True
        return False
