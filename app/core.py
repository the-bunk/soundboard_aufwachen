"""
app.core
~~~~~~~~~~~~~
core module
"""
import re
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security

db = SQLAlchemy()

security = Security()


def remove_html(input_str):
  r = re.compile('<.*?>')
  nohtml = re.sub(r, '', input_str)
  return nohtml
