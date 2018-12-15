from flask import Flask
from flask_session import Session
from app.core import db

import app.models as models_sounds
from .site import mod_site
# from app.mylogger import logger


app = Flask(__name__,  static_folder='static')
app.config.from_pyfile('config.py')

Session(app)

db.init_app(app)
db.create_all(app=app)  # app=app weil sonst applicationbound error

app.register_blueprint(mod_site)

app.jinja_env.globals.update(config=app.config)

def init_db():
    pass

# seed_security()
