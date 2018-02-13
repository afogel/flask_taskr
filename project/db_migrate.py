from views import db
from _config import DATABASE_PATH

import sqlite3
from datetime import datetime

with sqlite3.connect(DATABASE_PATH) as connection:
	cursor = connection.cursor()

	# THIS IS SO HACKY -- I NEED TO DUPLICATE MY ENTIRE TABLE AND THEN FEED IT IN???
	# GROSSSSSSSSSS
	# I also wish that this would occur in a single transaction so you can rollback quickly
	cursor.execute('ALTER TABLE tasks RENAME TO old_tasks')

	db.create_all()

	cursor.execute('''
		SELECT name, due_date, priority, status
		FROM old_tasks ORDER BY task_id ASC
	''')

	# posted_date is using datetime.now() instead of utcnow?
	# also, is it alright to backdate tasks as posted at now? Questions to ruminate on
	data = [(row[0], row[1], row[2], row[3], datetime.now(), 1) for row in cursor.fetchall()]

	cursor.executemany('''
		INSERT INTO tasks (name, due_date, priority, status, posted_date, account_id)
		VALUES (?, ?, ?, ?, ?, ?)
	''', data)

	# destroy old table...There has to be a more efficient way of doing this...
	cursor.execute('DROP TABLE old_tasks')