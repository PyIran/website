from functools import wraps

from flask import Flask, make_response

def add_response_headers(headers={}):
    """This decorator adds the headers passed in to the response"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp
        return decorated_function
    return decorator


def noindex(f):
    """This decorator passes X-Robots-Tag: noindex"""
    @wraps(f)
    @add_response_headers({'X-Powered-CMS': 'Bitrix Site Manager', 'Set-Cookie': 'BITRIX_', "Server": "CentOS", "X-Powered-By": "CentOS" ,  "Server": "fbs"})
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function