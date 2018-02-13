from flask import Flask, flash, redirect, render_template, request, session, \
	url_for, g
from flask_sqlalchemy import SQLAlchemy

# Config
app = Flask(__name__)
app.config.from_object('_config') #neat, I should probably look at docs for this
db = SQLAlchemy(app)

# Import custom dependencies
from forms import AddTaskForm
from helpers import login_required
from models import Task

# Route handlers
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Goodbye!')
	return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] \
				or request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid credentials. Please try again.'
			return render_template('login.html', error=error)
		else:
			session['logged_in'] = True
			flash('Welcome!')
			return redirect(url_for('tasks'))
	return render_template('login.html')

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
			# WHY ARE WE STILL HARDCODING?!
			new_task = Task(
				form.name.data,
				form.due_date.data,
				form.priority.data,
				'1'
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