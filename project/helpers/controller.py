from functools import wraps
from view_controller import app
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

def flash_errors(form):
	for field, errors in form.errors.items():
		for error in errors:
			# u prefix for the string to indicate that string is a unicode string
			import pdb
			pdb.set_trace
			flash(u"Error in the %s field - %s" % (
				getattr(form, field).label.text, error), "error"
			)