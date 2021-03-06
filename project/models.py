from view_controller import db

from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

class Task(db.Model):
	__tablename__ = 'tasks'

	task_id = db.Column(db.Integer, primary_key = True)
	account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

	due_date = db.Column(db.Date, nullable = False)
	name = db.Column(db.String, nullable = False)
	posted_date = db.Column(db.Date, default = datetime.utcnow())
	priority = db.Column(db.Integer, nullable = False)
	status = db.Column(db.Integer)

	def __init__(self, name, due_date, priority, posted_date, status, account_id):
		self.name = name
		self.due_date = due_date
		self.priority = priority
		self.posted_date = posted_date
		self.status = status
		self.account_id = account_id

	def __repr__(self):
		return '<name {0}>'.format(self.name)

	@hybrid_property
	def open(self):
		return self.status == '1'

	@hybrid_property
	def closed(self):
		return self.status == '0'


class Account(db.Model):

	__tablename__ = 'accounts'

	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String, unique = True, nullable = False)
	name = db.Column(db.String, unique = True, nullable = False)
	password = db.Column(db.String, nullable = False)
	tasks = db.relationship('Task', backref='poster')

	def __init__(self, name, email, password):
		self.name = name
		self.email = email
		self.password = password

	def __repr__(self):
		return '<account {0}>'.format(self.name)