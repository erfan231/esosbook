import os
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_wtf import CSRFProtect




app = Flask(__name__)
csrf = CSRFProtect(app)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

#app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
#app.config['WTF_CSRF_SECRET_KEY'] = "dkfjkgjfkgjkfdjk"
app.config['SESSION_TYPE'] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # os.environ.get("DB_URL)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # don't worry about this alot




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

app.config["MAIL_USERNAME"] = "esosbook@gmail.com" #os.environ.get("EMAIL_USERNAME")
app.config["MAIL_PASSWORD"] =  "erfanmahqw1@" #os.environ.get("MAIL_PASSWORD")

mail = Mail(app)


from esosbook import routes