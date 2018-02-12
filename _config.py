import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = True
# TODO: research and use env variable plugin to replace hard-coded secret key
SECRET_KEY = 'this is dumb' 

DATABASE_PATH = os.path.join(basedir, DATABASE)