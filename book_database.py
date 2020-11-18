from flask_sqlalchemy import SQLAlchemy 
import sqlite3
from flask import Flask
from flask_login import UserMixin


app = Flask(__name__)
app.config['SECRET_KEY'] = 'new_erfan'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # don't owrry about this alot

db = SQLAlchemy(app)
db.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    books = db.relationship("User_Books", backref="user") #this one looks for a class inside the python code
    #that's why we enter the name as User_Books


class All_Books(db.Model):
    __tablename__ = "all_books"
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(50), nullable=False, unique=True)
    author = db.Column(db.String(50))
    book_desc = db.Column(db.String(200))
    category = db.Column(db.String(50))


class User_Books(db.Model):
    __tablename__ = "user_books"
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(50), nullable=False, unique=True)
    author = db.Column(db.String(50))
    book_desc = db.Column(db.String(200))
    category = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id")) #this one looks inside the db
    #thats why i entered User as a all lowercase (user)




#create a connection between the user and the user_books
# create a connection between all books and user_books


if __name__ == "__main__":
    db.create_all()



"""


# if you don't have access to the object you can add to the database this way
  #current_user.username
user = User.query.filter_by(username="Erfan").first() # get the user
new_user_book = User_Books(book_name="Zero to One")
db.sesison.add(new_user_book)
db.sesion.commit()


# get all the user books
 #current_user.username
user_data = User.query.filter_by(username="Erfan").first()
user_data.username #users username
user_data.email #users email


#get the users books
user_data.books[0].username #this will get the first book that the user owns and the books name




"""