from flask import Blueprint

mod = Blueprint('user', __name__, url_prefix='/user')

from .login import *
from .dashboard import *
