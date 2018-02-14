from flask import Flask, flash, redirect, render_template, request, session, \
	url_for, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Config
app = Flask(__name__)
app.config.from_object('_config') #neat, I should probably look at docs for this
db = SQLAlchemy(app)

# Import custom dependencies
from forms import AddTaskForm, RegistrationForm, LoginForm
from helpers import login_required
from models import Task, Account

# Route handlers

@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			account = Account.query.filter_by(name=form.name.data).first()
			if account is not None and account.password == form.password.data:
				session['logged_in'] = True
				session['account_id'] = account.id
				flash('Welcome!')
				return redirect(url_for('tasks'))
			else:
				error = 'Invalid credentials. Please try again.'
		else:
			error = 'Both fields are required.'
	return render_template('login.html', form=form, error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.pop('account_id', None)
	flash('Goodbye!')
	return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	form = RegistrationForm(request.form)
	print(form.data)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_account = Account(
				form.name.data,
				form.email.data,
				form.password.data
			) # need to encrypt password
			db.session.add(new_account)
			db.session.commit()
			flash('Thanks for registering. Please login.')
			return redirect(url_for('login'))
	return render_template('register.html', form=form, error=error)

@app.route('/tasks/')
@login_required
def tasks():
	task_order = Task.due_date.asc()
	open_tasks = db.session.query(Task).filter_by(status='1').order_by(task_order)
	closed_tasks = db.session.query(Task).filter_by(status='0').order_by(task_order)
	return render_template(
		'tasks.html',
		form=AddTaskForm(request.form),
		open_tasks=open_tasks,
		closed_tasks=closed_tasks
	)

@app.route('/add', methods=['POST'])
@login_required
def new_task():
	form = AddTaskForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			# WHY ARE WE STILL HARDCODING?! (Now with MOAR hardcoding)
			new_task = Task(
				form.name.data,
				form.due_date.data,
				form.priority.data,
				datetime.utcnow(),
				'1',
				session['account_id']
			)
			db.session.add(new_task)
			db.session.commit()
			flash('New entry successfully posted. Thanks.')
			return redirect(url_for('tasks'))
		else:
			flash('All fields are required. Please try again.') 
			return redirect(url_for('tasks'))


@app.route('/complete/<int:task_id>')
@login_required
def complete(task_id):
	# remove magic number -- create more semantic way of of querying by status
	# scope?
	db.session.query(Task).filter_by(task_id = task_id).update({'status': '0'})
	db.session.commit()
	flash('The task was marked as complete. Dope.')
	return redirect(url_for('tasks'))

@app.route('/delete/<int:task_id>')
@login_required
def delete_entry(task_id):
	db.session.query(Task).filter_by(task_id=task_id).delete()
	db.session.commit()
	flash('The task was deleted.')
	return redirect(url_for('tasks'))
