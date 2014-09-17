#from python
import os
import sys
import logging
import logging.handlers

#from flask
from flask import Flask, request, jsonify, redirect, url_for, flash, g, session
from flask.ext.babel import Babel
from flask.ext.babel import gettext as _
from flask import request as r, g
import jinja2


#from project
from project.config import DefaultConfig as base_config
from project.utils.auth import GuestUser
from project.utils.template import render
from project.apps.user.models import Profile


from flask_wtf.csrf import CsrfProtect
csrf = CsrfProtect()

__all__ = ['create_app', 'create_simple_app']

DEFAULT_APP_NAME = 'project'


def create_app(config=None, app_name=DEFAULT_APP_NAME):
    """
    Tabe asli hast ke app ro misaze va configesh mikone.
    be in tabe tanzimate barname tahte name config ersal mishe va on tabzimat dar dakhele object
    app zakhire va negahdari mishe

    @param config: class ya objecte haviye tanzimate kolliye app mibashad.
    @param app_name: name asliye narm afzar
    """
    app = Flask(app_name)

    configure_app(app, config)
    configure_blueprints(app)
    configure_errorhandlers(app)
    configure_logger(app)
    configure_template(app)
    configure_user(app)
    configure_i18n(app)
    configure_site(app)
    configure_template_tag(app)
    csrf.init_app(app)
    return app


def configure_app(app, config):
    """
    tanzimate kolli app ke mamolan dar yek file zakhore mishavat tavasote in tabe
    megdar dehi va load mishavad
    """

    # config default ro dakhele app load mikone
    app.config.from_object(base_config())
    #sys.path.append(os.path.dirname(os.path.realpath(__file__)))
    if config is not None:
        # agar config degari be create_app ersal shode bashe dar in bakhsh load mishe
        # agar tanzimate in bakhsh gablan va dakhele defalt config tanzim shode bashe dobare nevisi mishe
        app.config.from_object(config)

    # dar sorati ke environment variable baraye tanzimat set shode bashe ham load mishe
    app.config.from_envvar('project_CONFIG', silent=True)


def configure_blueprints(app):
    """
    Tanzimate marbot be blueprint ha va load kardan ya nasbe onha ro inja anjam midim
    """

    app.config.setdefault('INSTALLED_BLUEPRINTS', [])
    blueprints = app.config['INSTALLED_BLUEPRINTS']
    for blueprint_name in blueprints:
        bp = __import__('project.apps.%s' % blueprint_name, fromlist=['views'])

        try:
            mod = __import__('project.%s'%blueprint_name, fromlist=['urls'])
        except ImportError:
            pass
        else:
            mod.urls.add_url_rules(bp.views.mod)
        try:
            app.register_blueprint(bp.views.mod)
        except:
            # report has no views
            pass

def configure_i18n(app):
    """
    tanzimate marbot be i18n va systeme tarjome dar in bakhsh emal mishavad
    """

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(['fa'])
        # return 'fa'
        # find set lang
        # TODO: user az inja gerefte mishe?!
        # aslan to in marhale user darim ma ya ye chize zafeyi hast?!
        user = getattr(g, 'user', None)
        if user is not None:
            pass
        accept_languages = app.config.get('ACCEPT_LANGUAGES', ['fa', 'en'])
        return request.accept_languages.best_match(accept_languages)

def configure_site(app):
    """
    """
    @app.context_processor
    def site_default():
        """
        """
        return {
            'site_name': app.config['SITE_NAME']
        }


def configure_errorhandlers(app):
    """
    tavasote in method baraye error haye asli va mamol khatahaye monaseb bargasht dade mishavad
    """

    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error):
        # import_cart_to_list(error)
        return render('base/404.html'), 404

    @app.errorhandler(403)
    def forbidden(error):
        # import_cart_to_list(error)
        return render('base/403.html'), 403

    @app.errorhandler(500)
    def server_error(error):
        # import_cart_to_list(error)
        return render('base/500.html'), 500

    @app.errorhandler(401)
    def unauthorized(error):
        # import_cart_to_list(error)
        return render('base/401.html'), 401

    @app.errorhandler(500)
    def internal_error(error):
        # import_cart_to_list(error)
        return render('base/500.html'), 500

    @app.errorhandler(400)
    def bad_gateway(error):
        # import_cart_to_list(error)
        return render('base/400.html'), 400

def configure_before_handlers(app):
    pass


def configure_template (app):
    """ Function doc """
    # g.tmp = 0
    base_dir = os.path.dirname(os.path.abspath(__file__))
    tmp_lst = []
    for item in app.config['TEMPLATE_DIR']:
        tmp_lst.append(base_dir + '/templates/' + item)
    tmp_lst=base_dir + '/templates/namin'
    tmp_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(tmp_lst),
    ])
    app.jinja_loader = tmp_loader  
    app.static_folder = base_dir + '/static'
  

 
def configure_logger(app):
    """
    This function Configure Logger for given Application.

    :param app: Application Object
    :type app: Object
    """

    # from project.utils.extended_logging import wrap_app_logger
    # wrap_app_logger(app)
    if app.debug or app.testing:
        from project.utils.extended_logging import wrap_app_logger
        wrap_app_logger(app)
        app.logger.create_logger('debuging')
        return

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    debug_file_handler = logging.handlers.RotatingFileHandler(
        app.config['DEBUG_LOG'],
        maxBytes=100000,
        backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_file_handler = logging.handlers.RotatingFileHandler(
        app.config['ERROR_LOG'],
        maxBytes=100000,
        backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)

 
def configure_user(app):
    """
    """

    @app.before_request
    def before_request():
        """
        """
        if 'username' in session:
            from project.apps.user.models import Profile
            try:
                g.user =  Profile.query.filter(Profile.username == session['username']).first()
            except:
                g.user = GuestUser()
        else:
            g.user = GuestUser()

def configure_template_tag(app):
    from project.utils.template_tag import init_filters
    init_filters(app)