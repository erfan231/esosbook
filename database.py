from flask_sqlalchemy import SQLAlchemy 
import sqlite3
from flask import Flask
from flask_login import UserMixin
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'new_erfan'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # don't owrry about this alot

db = SQLAlchemy(app)
db.init_app(app)

"""
#association table
    #                 table name
user_books = db.Table("user_books", db.Column(
"user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
db.Column("book_id",db.Integer, db.ForeignKey("books.book_id"), primary_key=True))
"""

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


    user_books = db.relationship('Books',
    secondary="user_books",
    lazy='dynamic',
    backref=db.backref('user', lazy='dynamic'))

    usr_fav_books = db.relationship('Books',
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
    book_desc = db.Column(db.String(200))
    category = db.Column(db.String(50))
    time_stamp = db.Column(db.DateTime(timezone=True), default=time.localtime())


    users = db.relationship("Users", secondary="user_books")
    users = db.relationship("Users", secondary="user_fav_books")



#association table
class User_Books(db.Model):
    __tablename__="user_books"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))

    users = db.relationship(Users, backref=db.backref("User_Books",cascade="all, delete-orphan"))
    books = db.relationship(Books, backref=db.backref("User_Books", cascade="all,delete-orphan"))


class User_fav_books(db.Model):
    __tablename__ = "user_fav_books"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))

    users = db.relationship(Users, backref=db.backref("User_fav_books",cascade="all, delete-orphan"))
    books = db.relationship(Books, backref=db.backref("User_fav_books", cascade="all,delete-orphan"))

if __name__ == "__main__":
    db.create_all()


else:
    pass

    """


    # if you don't have access to the object you can add to the database this way
    #current_user.username
    user = User.query.filter_by(username="Erfan").first() # get the user
    new_user_book = User_Books(book_name="Zero to One")
    db.sesison.add(new_user_book)
    db.sesion.commit()


    # query.filter_by(username="Erfan").first()
    user_data.username #users username
    user_data.email #users email


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



    #user = Users.query.first()
    #user.products  # List all products, eg [<productA>, <productB> ]
    #user.orders    # List all orders, eg [<order1>, <order2>]
    #user.orders[0].products  # List products from the first order

metadata = MetaData()

example = Table('example', metadata,
    Column('id', Integer, primary_key=True),
    Column('date', DateTime(timezone=True), default=time.utc.now()))


  """



    #user = Users.query.first()
    #user.products  # List all products, eg [<productA>, <productB> ]
    #user.orders    # List all orders, eg [<order1>, <order2>]
    #user.orders[0].products  # List products from the first order

    #p1 = Product.query.first()
    #p1.users  # List all users who have bought this product, eg [<user1>, <user2>]