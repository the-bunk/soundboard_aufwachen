from os import path
from flask import Flask
from flask_security import current_user
from flask_session import Session
from app.core import db, security

import app.models as models_sounds
from .site import mod_site
import app.admin.models_security as models_security
from .admin import mod_admin


app = Flask(__name__,  static_folder='static')
app.config.from_pyfile('config.py')

Session(app)

db.init_app(app)
db.create_all(app=app)  # app=app weil sonst applicationbound error

security.init_app(app, models_security.user_datastore)

app.register_blueprint(mod_admin, url_prefix='/admin')
app.register_blueprint(mod_site)

app.jinja_env.globals.update(config=app.config)
app.jinja_env.globals.update(current_user=current_user)
app.jinja_env.globals.update(path=path)


# seed_security()
