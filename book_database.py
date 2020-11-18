from flask_sqlalchemy import SQLAlchemy 
import sqlite3
from flask import Flask, UserMixin


app = Flask(__name__)
app.config['SECRET_KEY'] = 'new_erfan'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # don't owrry about this alot

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


class All_Books(db.Model):
    __tablename__ = "all_books"
    id = db.Model(db.Integer, primary_key=True)
    book_name = db.Model(db.String(50), nullable=False, unique=True)
    author = db.Model(db.String(50))
    book_desc = db.Model(db.String(200))
    category = db.Model(db.String(50))


class Books_Read(db.Model):
    __tablename__ = "book_read"
    id = db.Model(db.Integer, primary_key=True)
    book_name = db.Model(db.String(50), nullable=False, unique=True)
    author = db.Model(db.String(50))
    book_desc = db.Model(db.String(200))
    category = db.Model(db.String(50))





