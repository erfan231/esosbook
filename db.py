# NEW DB STRUCTURE
from flask_sqlalchemy import SQLAlchemy 
import sqlite3
from flask import Flask
from flask_login import UserMixin
import datetime



app = Flask(__name__)
app.config['SECRET_KEY'] = 'new_erfan'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # don't worry about this alot

db = SQLAlchemy(app)
db.init_app(app)



class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


    user_books = db.relationship('Books',
    secondary="user_books",
    lazy='dynamic',
    backref=db.backref('user', lazy='dynamic'))

    user_fav_books = db.relationship('Books',
    secondary="user_fav_books",
    lazy='dynamic',
    backref=db.backref('usr_favorite', lazy='dynamic'))



#what is the relationship between the user and All_Books?
# well the user can create an order(book) from all books
class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(50), nullable=False, unique=True)
    author = db.Column(db.String(50))
    category = db.Column(db.String(50))

    #secondary needs to refer to a Table object, not a mapped class, if by string name then it would be lowercase
    users = db.relationship("Users", secondary="user_books")
    users = db.relationship("Users", secondary="user_fav_books")



#association table
class User_Books(db.Model):
    __tablename__="user_books"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_summary = db.Column(db.String())
    time_added = db.Column(db.Date, default=datetime.datetime.now())
    last_updated = db.Column(db.Date, default=datetime.datetime.now())

    users = db.relationship(Users, backref=db.backref("User_Books",cascade="all, delete-orphan"))
    books = db.relationship(Books, backref=db.backref("User_Books", cascade="all,delete-orphan"))

    #add user_fav bo


class User_fav_books(db.Model):
    __tablename__ = "user_fav_books"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    book_summary = db.Column(db.String())
    time_added = db.Column(db.Date, default=datetime.datetime.now())
    last_updated = db.Column(db.Date, default=datetime.datetime.now())

    users = db.relationship(Users, backref=db.backref("User_fav_books",cascade="all, delete-orphan"))
    books = db.relationship(Books, backref=db.backref("User_fav_books", cascade="all,delete-orphan"))
    
    #add user books relationship




db.create_all()