# coding: utf-8
from datetime import datetime
from dateutil import relativedelta

from persian import english_num_to_persian
from flask import g, request, url_for
from flask.ext.babel import gettext as _

from .date import gregorian_to_jalali
from .template import is_ajax

# new function for jinja2  :D

def persian_num(value):
    return english_num_to_persian(value)

def jalali(value):
    return gregorian_to_jalali(value)
    if not value:
        return ''

    datelist = gregorian_to_jalali(value).split("/")
    datelist[1] = PERSIAN_MON[int(datelist[1]) - 1]
    return " ".join(datelist)

def time_to_jalali(value):
    if not value:
        return ''

    datelist = gregorian_to_jalali(datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f'))
    # datelist[1] = PERSIAN_MON[int(datelist[1]) - 1]
    return datelist, value.split(' ')[1].split('.')[0]

def now():
    return gregorian_to_jalali(datetime.now())

def group(*roles):
    for item in roles:
        request_role = Roles.query.filter(Roles.role_name == item).first()
        try:
            user_have_role =  User_Role.query.filter(
                User_Role.role == request_role.id ,
                User_Role.user == g.user.id  
                ).first()
            if user_have_role:
                return True
        except:
            pass
    return False    

def year(y1, y2):
    if not y2:
        y2 = datetime.now()
    if not y1:
        return ""
    diff = relativedelta.relativedelta(y2, y1)
    result = ""
    if diff.years:
        result += "%s %s" % (diff.years, _("years"))
    if diff.months:
        if result:
            result += _(" and ")
        result += "%s %s" % (diff.months, _("mouths"))
    if not result:
        return ""
    return "(" + result + ")"


def append_get_url(**new_args):
    args = request.args.copy()
    for item in new_args.keys():
        if item in args:
            del args[item]
    args.update(new_args)
    return url_for(request.endpoint, **args)

def ref_url():
    ref_url = (request.path)
    return ref_url


def __dir(obj):
    return dir(obj)

def init_filters(app):
    app.jinja_env.globals['jalali'] = jalali
    app.jinja_env.globals['year'] = year
    app.jinja_env.globals['is_ajax'] = is_ajax
    app.jinja_env.globals['now'] = now
    app.jinja_env.globals['append_get_url'] = append_get_url
    app.jinja_env.globals['group'] = group
    app.jinja_env.globals['ref_url'] = ref_url
    app.jinja_env.globals['time_to_jalali'] = time_to_jalali
    app.jinja_env.globals['persian_num'] = persian_num
    app.jinja_env.globals['dir'] = __dir