import os
TITLE = "Aufwachen Podcast Soundboard"
APP_PATH = os.path.dirname(os.path.realpath(__file__))
DEBUG = True
DATABASE = 'sqlite:///test.db'  # relativer pfad
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # relativer pfad
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO=False

SECRET_KEY = "e89ashdjsahb"
SESSION_TYPE = 'filesystem'  # ist das okay?

SECURITY_REGISTERABLE = False
SECURITY_EMAIL_SENDER = 'soundboard.bot@web.de'
SECURITY_CONFIRMABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE= True
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_TRACKABLE = True
SECURITY_PASSWORD_SALT = ''
SECRET_KEY = ''

MAIL_SERVER = 'smtp.web.de'
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME = 'soundboard.bot@web.de'
MAIL_PASSWORD = ''

MAIN_STATIC_DIR = 'app/static'
SOUNDS_DIR = 'app/static/sounds'
MAX_CONTENT_LENGTH = 1 * 1024 * 1024
