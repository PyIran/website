from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from project.database import Base
from project.database import db_session
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from flask.ext.babel import lazy_gettext as _

# FIXME: move to extensions
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Roles(Base):
	__tablename__ = 'role'
	id = Column(Integer, primary_key=True)
	role_name = Column(String(50), unique=True, nullable=False, info={'label': _('role name')})
	url = Column(String(250), nullable=False, info={'label': _('website')})
	parent = Column(Integer, nullable=False, info={'label': _('parent')})
	description = Column(String(50), info={'label': _('description')})

	def __init__(self, **kwargs):
		super(Roles, self).__init__(**kwargs)	

	def __repr__(self):
		return self.role_name


class User_Role(Base):
	__tablename__ = 'user_role'
	id = Column(Integer, primary_key=True)
	role =  Column(Integer,ForeignKey('role.id'), info={'label': _('role')})
	user =  Column(Integer,ForeignKey('profile.id'), info={'label': _('user')})

	def __init__(self, **kwargs):
		super(User_Role, self).__init__(**kwargs)	

	def __repr__(self):
		return self.role

class Profile(Base):
	__tablename__ = 'profile'
	id = Column(Integer, primary_key=True)
	username = Column(String(50), unique=True, nullable=False, info={'label': _('username')})
	password = Column(String(100), nullable=False, info={'label': _('password')})
	group_list = Column(String(50), info={'label': _('group list')})
	phone = Column(String(50), info={'label': _('phone')})
	email = Column(EmailType, info={'label': _('email')})
	registered_at = Column(String(50), info={'label': _('registered at')})

	
	firstName = Column(String(50), info={'label': _('first name')})
	lastName = Column(String(50), info={'label': _('last name')})
	sex = Column(Boolean, info={'label': _('sex')})
	birthday = Column(String(50), info={'label': _('birthday')})
	avatar = Column(String(50), info={'label': _('avatar')})
	country = Column(String(50), info={'label': _('country')})
	city = Column(String(50), info={'label': _('city')})

	creator = Column(Integer, info={'label': _('creator')})

	def __init__(self, **kwargs):
		super(Profile, self).__init__(**kwargs)	

	def __repr__(self):
		return self.username

	def can(self, roles):
		for item in roles:
			request_role = Roles.query.filter(Roles.role_name == item).first()
			try:
				user_have_role =  User_Role.query.filter(
					User_Role.role == request_role.id ,
					User_Role.user == self.id  
					).first()
				if user_have_role:
					return True
			except:
				pass
		return False

	def has_group(self, group):
		"""
		"""
		if group == self.group_list:
			return True
		return False

	def __unicode__(self):
		return self.username

class Log(Base):
	'''
	table log
	'''
	__tablename__ = 'log_actions'
	id = Column(Integer, primary_key=True)
	log_date = Column(String(50), nullable=False, info={'label': _('date')})
	log_desc = Column(String(300), info={'label': _('description')})
	log_user = Column(Integer, ForeignKey('profile.id'),info={'label': _('user name')})
	user = relationship(
		Profile,
		# backref='profile' 
		)
	def __init__(self, **kwargs):
		super(Log, self).__init__(**kwargs)	

	def __repr__(self):
		return self.log_desc
