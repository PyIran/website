# coding: utf-8

import datetime

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker

import imp
from migrate.versioning import api

engine = create_engine('sqlite:///pyiran.db', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///pyiran.db'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	# import all modules here that might define models so that
	# they will be registered properly on the metadata.  Otherwise
	# you will have to import them first before calling init_db()

	Base.metadata.create_all(bind=engine)
	if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
		api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
		api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	else:
		api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))    

	newdb()

def migrate():
	migration = SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_migration.py' % (api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO) + 1)
	tmp_module = imp.new_module('old_model')
	old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	exec old_model in tmp_module.__dict__
	script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, Base.metadata)
	open(migration, "wt").write(script)
	api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	print 'New migration saved as ' + migration
	print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))	

def newdb():
	from apps.user.models import Profile, Roles, User_Role
	session = db_session()
	session._model_changes = {}
	admin=Profile(
		username="admin",
		password="pbkdf2:sha1:1000$FWFdPAeH$6cf64b6fa1308fb1bc8baf799d13100f467040d7",
		group_list="admin"
	)
	session.add(admin)
	role=Roles(role_name="pyiran", parent=-1, description="developer", url="")
	session.add(role)
	role=Roles(role_name="admin", parent=0, description="sysadmin", url="")
	session.add(role)
	role=Roles(role_name="login", parent=0, description="enabeled user", url="")
	session.add(role)
	userrole=User_Role(user=1,role=1)
	session.add(userrole)
	userrole=User_Role(user=1,role=2)
	session.add(userrole)
	userrole=User_Role(user=1,role=3)
	session.add(userrole)
	session.commit()	