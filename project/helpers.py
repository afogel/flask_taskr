from functools import wraps
from views import app
from flask import flash, redirect, session, url_for

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash("You need to login first.")
			return redirect(url_for('login'))
	return wrap