from flask import Flask, url_for
from config import Config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from app.utils import User

UPLOAD_FOLDER = "app/static/img/".replace('/', '\\')
app = Flask(__name__)
app.config.from_object(Config)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['USER'] = User(-1 ,"", "", "no_auth", "")
bootstrap = Bootstrap(app)
login = LoginManager(app)

from app import routes