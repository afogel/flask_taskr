from flask import Flask, flash, redirect, render_template, request, session, \
	url_for, g

# Config
app = Flask(__name__)
app.config.from_object('_config') #neat, I should probably look at docs for this

# Import custom dependencies
from forms import AddTaskForm
from helpers import connect_db, login_required

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
	# Pretty onerous to have to explicitly call using SQL. WHERE IS THE ORM?!
	g.db = connect_db()
	cursor = g.db.execute('''
		SELECT name, due_date, priority, task_id FROM tasks WHERE status=1
	''')
	open_tasks = [
		dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) \
			for row in cursor.fetchall()
	]

	cursor = g.db.execute('''
		SELECT name, due_date, priority, task_id FROM tasks WHERE status=0
	''')
	closed_tasks = [
		dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) \
			for row in cursor.fetchall()
	]
	g.db.close()
	return render_template(
		'tasks.html',
		form=AddTaskForm(request.form),
		open_tasks=open_tasks,
		closed_tasks=closed_tasks
	)

@app.route('/add', methods=['POST'])
@login_required
def new_task():
	form = request.form
	name, due_date, priority = form['name'], form['due_date'], form['priority']

	# manual backend validation
	if not name or not due_date or not priority:
		flash('All fields are required. Please try again.') 
		return redirect(url_for('tasks.html'))
	else:
		g.db = connect_db()
		# I don't love the hard-coded magic number here -- would be better to have 
		# default value set in create_DB migration
		g.db.execute(
			'INSERT INTO tasks (name, due_date, priority, status) VALUES (?, ?, ?, 1)',
			[name, due_date, priority]
		)
		g.db.commit()
		g.db.close()
		flash('New entry successfully posted. Thanks.')
		return redirect(url_for('tasks'))


@app.route('/complete/<int:task_id>')
@login_required
def complete(task_id):
	g.db = connect_db()
	g.db.execute('UPDATE tasks SET status = 0 WHERE task_id = ?', task_id)
	g.db.commit()
	g.db.close()
	flash('The task was marked as complete.')
	return redirect(url_for('tasks'))

@app.route('/delete/<int:task_id>')
@login_required
def delete_entry(task_id):
	g.db = connect_db()
	g.db.execute('DELETE tasks SET status = 0 WHERE task_id = ?', task_id)
	g.db.commit()
	g.db.close()
	flash('The task was deleted.')
	return redirect(url_for('tasks'))