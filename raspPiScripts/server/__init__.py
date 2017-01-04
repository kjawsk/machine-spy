import os
from flask import Flask
from server.models import db
from flask_login import LoginManager

app = Flask(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='sqlite:///server.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    DEBUG=True,
    SECRET_KEY=os.urandom(24)
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
db.init_app(app)
db.app = app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

import server.api
import server.views
