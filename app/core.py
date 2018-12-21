"""
app.core
~~~~~~~~~~~~~
core module
"""
import re
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_mail import Mail

db = SQLAlchemy()

mail = Mail()

security = Security()


def remove_html(input_str):
  r = re.compile('<.*?>')
  nohtml = re.sub(r, '', input_str)
  return nohtml
