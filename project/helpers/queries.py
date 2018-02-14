from view_controller import db
from models import Task

def open_tasks():
	return db.session.query(Task).filter(Task.open).order_by(Task.due_date.asc())

def closed_tasks():
	return db.session.query(Task).filter(Task.closed).order_by(Task.due_date.asc())