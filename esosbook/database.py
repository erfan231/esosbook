
import datetime

from flask import Flask, current_app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from esosbook import db


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)

    user_books = db.relationship('Books',
                                 secondary="user_books",
                                 lazy='dynamic',
                                 backref=db.backref('user', lazy='dynamic'))

    user_fav_books = db.relationship('Books',
                                     secondary="user_fav_books",
                                     lazy='dynamic',
                                     backref=db.backref('usr_favorite', lazy='dynamic'))


class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50))
    category = db.Column(db.String(50))
    owner = db.Column(db.Integer, db.ForeignKey("users.id"))

    # secondary needs to refer to a Table object, not a mapped class, if by string name then it would be lowercase
    users = db.relationship("Users", secondary="user_books")
    users = db.relationship("Users", secondary="user_fav_books")
    users = db.relationship(Users, backref=db.backref("Books", cascade="all, delete-orphan"))


# association table
class User_Books(db.Model):
    __tablename__ = "user_books"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_summary = db.Column(db.String())
    time_added = db.Column(db.Date, default=datetime.datetime.now())
    last_updated = db.Column(db.Date, default=datetime.datetime.now())

    users = db.relationship(Users, backref=db.backref("User_Books", cascade="all, delete-orphan"))
    books = db.relationship(Books, backref=db.backref("User_Books", cascade="all,delete-orphan"))

    # add user_fav bo


class User_fav_books(db.Model):
    __tablename__ = "user_fav_books"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    book_summary = db.Column(db.String())
    time_added = db.Column(db.Date, default=datetime.datetime.now())
    last_updated = db.Column(db.Date, default=datetime.datetime.now())
    book_img_url = db.Column(db.String())


    users = db.relationship(Users, backref=db.backref("User_fav_books", cascade="all, delete-orphan"))
    books = db.relationship(Books, backref=db.backref("User_fav_books", cascade="all,delete-orphan"))

    # add user books relationship


db.create_all()