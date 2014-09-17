# from python
import re
import urllib

# from wtforms
from wtforms import IntegerField, TextField, PasswordField, BooleanField, TextAreaField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, Email, optional, EqualTo
from wtforms.ext.i18n.utils import get_translations

# from flask
from flask import g
from flask.ext.wtf import Form
from flask.ext.babel import lazy_gettext as _

from project.utils.form import JalaliDate, jDateField

#from friendfile
#from friendfile.models import Entity
from project.apps.user.models import Profile
from wtforms_alchemy import model_form_factory
from project.database import Base
from project.database import db_session as db

BaseModelForm = model_form_factory(Form)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
		session = db()
		session._model_changes = {}
		return session

translations_cache = {}


class LoginForm(Form):
    username = TextField(
        _('username'),
        [DataRequired(),
         Length(min=4,max=25)]
    )
    password = PasswordField(_('password'), [
        DataRequired(),Length(min=4,max=25)
    ])
    remember = BooleanField(_('remember'))
    
    LANGUAGES = ['fa']
    def _get_translations(self):
        languages = tuple(self.LANGUAGES) if self.LANGUAGES else None
        if languages not in translations_cache:
            translations_cache[languages] = get_translations(languages)
        return translations_cache[languages]