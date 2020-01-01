from flask import Flask, url_for
from config import Config
from flask_bootstrap import Bootstrap

UPLOAD_FOLDER = "app/static/img/".replace('/', '\\')
app = Flask(__name__)
app.config.from_object(Config)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bootstrap = Bootstrap(app)

from app import routes