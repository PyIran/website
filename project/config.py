#coding: utf-8
import os

# Read all apps and add to blueprint
def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

class DefaultConfig(object):
	DEBUG = True
	DEPLOYMENT = False

	ACCEPT_LANGUAGES = ['fa', 'en']

	BABEL_DEFAULT_LOCALE = 'fa'
	BABEL_DEFAULT_TIMEZONE = 'Asia/tehran'

	CSRF_ENABLED = True
	SECRET_KEY = '\x05m\xa8\x8b\r\xd94\xc7\x81\x99\xdb\x06<-cwT\x0fk'\
		'\x88\xb9\xb6\x18\xceV\x89\xb8&*\x06\xe8\xde'

	TEMP_FOLDER = "%s/temp/" % os.path.dirname(os.path.abspath(__file__))
	UPLOAD_FOLDER = "%s/upload/" % os.path.dirname(os.path.abspath(__file__))

	SITE_NAME = u'گروه کاربران پایتون ایران'
	logger_name = 'pos_acc'
	# Blueprint haye nasb shode dar app bayad be in list ezafe beshan
	INSTALLED_BLUEPRINTS = tuple(get_immediate_subdirectories('project/apps'))
	TEMPLATE_DIR = list(get_immediate_subdirectories('project/templates'))
	LOGGER_NAME = 'pyiran'
	LOG_PATH = '/var/log/pyiran/'  # '/var/log/project/'
	DEBUG_LOG = LOG_PATH + "debug.log"
	ERROR_LOG = LOG_PATH + "error.log"

	VIRSION = 0.11

	# RF_READER_ADD = '192.168.0.7'
	# RF_READER_PORT = 1001

	if DEBUG:
		LOG_FORMAT = '\033[1;35m[%(asctime)s]\033[1;m [\033[1;31m %(levelname)s \033[1;m] \033[1;32m[%(logger_name)s]\033[1;m: \
		\033[1;33m %(message)s \033[1;m'
	else:
		LOG_FORMAT = '[%(asctime)s] %(levelname)s [%(logger_name)s]: %(message)s'

class DeploymentConfig(DefaultConfig):
    DEBUG = False
    TESTING = False
    DEPLOYMENT = True


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    CACHE_TYPE = 'null'
    #PROPAGATE_EXCEPTIONS = True
