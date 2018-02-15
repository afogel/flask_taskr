import os
import unittest

from viewscontroller import app, db
from _config import basedir
from models import Account

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):
	def setup(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
			basedir, TEST_DB
		)
		self.app = app.test_client()
		db.create_all()

	def tear_down(self):
		db.session.remove()
		db.drop_all()


if __name__ == '__main__':
	unittest.main()
