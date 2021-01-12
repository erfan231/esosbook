import os
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_wtf import CSRFProtect
import json



app = Flask(__name__)
csrf = CSRFProtect(app)


with open("/esos/config.json" ) as config_file:
        config = json.load(config_file) #python dict

app.config.update(dict(
    SECRET_KEY=config.get("SECRET_KEY"),
    WTF_CSRF_SECRET_KEY=config.get("WTF_CSRF_SECRET_KEY"),
    SESSION_TYPE = "filesystem",
    SQLALCHEMY_DATABASE_URI = config.get("DB_URI"),
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    MAIL_USERNAME = config.get("MAIL_USERNAME"),
    MAIL_PASSWORD = config.get("MAIL_PASSWORD")


))




db = SQLAlchemy(app)
db.init_app(app)


bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False


mail = Mail(app)
from esosbook import routes