import os
import unittest
import pdb

from view_controller import app, db
from _config import basedir
from models import Account

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
			basedir, TEST_DB
		)
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_from_is_present(self):
		pdb.set_trace()
		register = self.app.get('/')


if __name__ == '__main__':
	unittest.main()
