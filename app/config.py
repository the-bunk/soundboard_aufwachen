import os
TITLE = "Aufwachen Podcast Soundboard"
APP_PATH = os.path.dirname(os.path.realpath(__file__))
DEBUG = True
DATABASE = 'sqlite:///test.db'  # relativer pfad
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # relativer pfad
SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_ECHO=True

SECRET_KEY = "e89ashdjsahb"
SESSION_TYPE = 'filesystem'  # ist das okay?

SECURITY_REGISTERABLE = True
SECURITY_EMAIL_SENDER = 'the_bunk@gmx.de'
SECURITY_CONFIRMABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE= True
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_TRACKABLE = True
SECURITY_PASSWORD_SALT = 'sadjLkSac")2}2X7GrsJFn6:3\'t{82Eb/EhL@^@,)=/w{RAj2)RrW*A)/LWQ*%(j[c79Hx5['
SECRET_KEY = 'super-secret>yA#Bb{7\'bf`$g_{\M5vQYE2w3dDW'

SOUNDS_DIR = 'app/static/sounds'
MAX_CONTENT_LENGTH = 1 * 1024 * 1024
