# python import
import os
import time
from hashlib import sha1
from random import random

from flask import abort
from flask.ext.babel import lazy_gettext as _
from project.libs.wtf import DateTimeField
from werkzeug import secure_filename

from .date import gregorian_to_jalali, jalali_to_gregorian, parser

# add DRM lib to add watermark/hash and save to DB

ALLOWED_EXTENSIONS = set(
    ['txt',
     'pdf',
     'png',
     'jpg',
     'jpeg',
     'gif',
     'doc',
     'docx',
     'xlsx'])


def check_file(form, field):
    if field.data:
        filename = field.data.lower()
        ALLOWED_EXTENSIONS = set(['jpg'])
        # TODO must be go in config
        if not ('.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS):
            raise form.validators.ValidationError(
                _('Wrong Filetype, you can upload only png,jpg,jpeg,gif files'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_db_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['zip']
 

def file_ext(file_name):
    name, ext = os.path.splitext(file_name)
    return ext


def random_filename():
    code = sha1()
    code.update(str(random()))
    hex_code = code.hexdigest()
    return hex_code


def exists_or_create(path):
    if not os.path.exists(path):
        os.makedirs(path)

class TagWidget(object):
    html = """<input name="%s" id="%s" value="%s">
    <script type="text/javascript">
    $(function(){$("\#%s").tagit({autocomplete: {source: '%s', minLength: 3}});});
    </script>
    """

    def __init__(self, uri, input_type='submit'):
        self.uri = uri
        self.input_type = input_type

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        data = ""
        if field.data:
            data = field.data
        return self.html % (field.id, field.name, data, field.id, self.uri)
        
class AutocompleteWidget(object):
    html = """
    <input class="%s" name="%s" type="text" value="%s">
    <script type="text/javascript">
    $('.%s').autocomplete({source: '%s', minLength: 3 %s});
    </script>
    """

    force_html = """    """

    def __init__(self, uri, force=False, input_type='text'):
        self.force = force
        self.uri = uri
        if input_type is not None:
            self.input_type = input_type

    def __call__(self, field, **kwargs):
        self.id = str(time.time()).replace('.', '_') + field.id
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        data = ""
        if field.data:
            data = field.data
        return (
            self.html % (
                self.id,
                field.id,
                data,
                self.id,
                self.uri,
                self.force_html if self.force else "")
        )


class JalaliDate(object):
    html = """
    <input class="has_datepicker" name="%s" type="text" value="%s">
    <script type="text/javascript">
    $('.has_datepicker').datepicker({dateFormat: 'yy/mm/dd', changeMonth: true, changeYear: true, yearRange: '1310:1400'});
    </script>
    """

    def __init__(self, input_type='text'):
        if input_type is not None:
            self.input_type = input_type

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        data = ""
        if field.data:
            data = gregorian_to_jalali(field.data)
        return self.html % (field.id, data)


class jDateField(DateTimeField):

    """
    Same as DateTimeField, except stores a `datetime.date`.
    """

    def __init__(self, label=None, validators=None,
                 format='%Y-%m-%d', **kwargs):
        super(jDateField, self).__init__(label, validators, format, **kwargs)

    def _value(self):
        if self.raw_data:
            return ' '.join(self.raw_data)
        else:
            if isinstance(self.data, unicode):
                return parser(self.data)
            else:
                return self.data and self.data.strftime(self.format) or ''

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                self.data = jalali_to_gregorian(date_str)
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid date value'))
