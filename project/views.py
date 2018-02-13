import sqlite3 # why is my view-controller querying the db?

from flask import Flask, flash, redirect, render_template, request, session \
	url_for

from helpers import connect_db, login_required

# Config
app = Flask(__name__)
app.config.from_object('_config') #neat, I should probably look at docs for this

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

