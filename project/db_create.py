
from view_controller import db
from models import Task
from datetime import date

db.create_all()

# for status, 1 == 'open'; this is a dumb schema, but whatever. Tutorials, man.
db.session.add(Task("Finish this tutorial", date(2018,3,25), 10, 1))
db.session.add(Task("Finish Real Python Course", date(2018,3,25), 10, 1))

db.session.commit()
