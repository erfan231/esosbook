from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db import app, db, Users, Books, User_Books
from forms import *
from sqlalchemy.exc import IntegrityError
import requests

db.create_all()

host = "10.254.25.197"
port = 5000

bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    # default values
    form = PostForm()
    user_books = User_Books.query.filter_by(user_id=current_user.id).all()
    user_books_table = user_books
# try:
    user = Users.query.filter_by(username=str(current_user.username)).first() 

    books = user.user_books
    book_num = books.count()

    fav_books = user.usr_fav_books #get the fav books using table relationships between user and fav_books
    fav_book_num = fav_books.count()

    if form.validate_on_submit():
        try:
            new_book_created = Books(book_name=form.Title.data, author=form.Author.data,
                                    category=form.Category.data)
            db.session.add(new_book_created)
            db.session.commit()
            add_to_user_book = User_Books(book_id=new_book_created.id,book_summary=form.Summary.data,user_id=current_user.id)
            db.session.add(add_to_user_book)
            db.session.commit()
            flash("new book added", "success")
            return redirect("dashboard")
        except:
            db.session.rollback()
            db.session.commit()
        finally:
            pass
    # except:
    #   flash("An error occured when trying to get your books", "danger")
    return render_template('dashboard.html', name=current_user.username,
                           books=books, num_of_books=book_num, fav_book_num=fav_book_num,
                           fav_books=fav_books, ub=user_books_table,form=form)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect("/dashboard")
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = Users.query.filter_by(username=form.username.data).first()
        except:
            flash("An error occured, please try again later", "danger")
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid Credential, Try again", "warning")
        else:
            flash("user don't exists, Please Sign Up", "warning")

        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.confirm_password.data:
            hashed_password = generate_password_hash(
                form.password.data, method='sha256')
            new_user = Users(username=form.username.data,
                             email=form.email.data, password=hashed_password)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("User  {} has been sucessfully created!".format(str(form.username.data)), "success")

                return redirect("login")
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
            except IntegrityError as error:
                flash("User already exists. Please login instead", "warning")
        flash("Password doesn't match", "warning")

    return render_template('signup.html', form=form)


@app.route("/user")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/book_new", methods=["POST", "GET"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
            new_book_created = Books(book_name=form.Title.data, author=form.Author.data,
                                    category=form.Category.data)
            db.session.add(new_book_created)
            db.session.commit()
            flash("new book added", "success")
            add_to_user_book = User_Books(book_id=new_book_created.id,book_summary=form.Summary.data,user_id=current_user.id)
            db.session.add(add_to_user_book)
            db.session.commit()
            return redirect("dashboard")
        except:
            db.session.rollback()
            db.session.commit()
        finally:
            pass
            

       
    return render_template("book_new.html", form=form)


@app.route("/delete/<int:id>")
def delete(id):
    delete_book = User_Books.query.get_or_404(id)

    try:
        db.session.delete(delete_book)
        db.session.commit()
        flash("Book Deleted successfully!", "success")
        return redirect("/dashboard")
    except:
        flash("Couldn't delete your book, please try again", "warning")
        return redirect("/dashboard")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


"""
@app.route("/export")
def export():
    #data = zip(Book_titles,Book_prices)
    return render_template("export_books.html", data=("book", "idk"))
"""



@app.route("/testform", methods=['GET', 'POST'])
def form():
    
    return render_template('test_forms.html')

if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)
