import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
	
	# get a cursor object to execute queries
	cursor = connection.cursor()

	cursor.execute("DROP TABLE IF EXISTS tasks;")
	cursor.execute(
		'''
		CREATE TABLE tasks(
			task_id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			due_date TEXT NOT NULL,
			priority INTEGER NOT NULL,
			status INTEGER NOT NULL
		)
		'''
	)

	# Dummy data
	# for status, 1 == 'open'; this is a dumb schema, but whatever. Tutorials, man.
	cursor.execute('''
		INSERT INTO tasks(name, due_date, priority, status) 
		VALUES("Finish this tutorial", "03/25/2018", 10, 1)
	''')
	cursor.execute('''
		INSERT INTO tasks(name, due_date, priority, status) 
		VALUES("Finish Real Python Course", "03/25/2018", 10, 1)
	''')

