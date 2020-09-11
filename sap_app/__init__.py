from os import environ, path
from flask import Flask
from flask.json import JSONEncoder
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_httpauth import HTTPTokenAuth





basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

app = Flask(__name__)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['SECRET_KEY'] = environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Bearer')



from sap_app import routes