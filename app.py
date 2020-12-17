from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db import app, db, Users, Books, User_Books
from forms import *
from sqlalchemy.exc import IntegrityError
import datetime


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


@app.route('/')
def index():
    return render_template('index.html',user_legged_in_already=current_user.is_authenticated)


@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    # default values
    form = PostForm()
    updateform = UpdateForm()
    user_books = User_Books.query.filter_by(user_id=current_user.id).all()
    ub = user_books
   
# try:
    user = Users.query.filter_by(username=str(current_user.username)).first()

    books = user.user_books
    book_num = books.count()

    fav_books = user.user_fav_books  # get the fav books using table relationships between user and fav_books
    fav_book_num = fav_books.count()

    # adding books modal
    if form.validate_on_submit():
        
        new_book_created = Books(book_name=form.Title.data, author=form.Author.data,
                                    category=form.Category.data, owner=current_user.id)
        db.session.add(new_book_created)
        db.session.commit()
        add_to_user_book = User_Books(book_id=new_book_created.id,
                                        book_summary=form.Summary.data, user_id=current_user.id,time_added=datetime.datetime.now(),last_updated=datetime.datetime.now())
        db.session.add(add_to_user_book)
        db.session.commit()
        #flash("{} has been added successfully to your book collection".format(form.Title.data), "success")
        return redirect("dashboard")
    
        db.session.rollback()
        #flash("error occured", "warning")
    
        db.session.commit()
    # except:
    #   flash("An error occured when trying to get your books", "danger")
    return render_template('dashboard.html', name=current_user.username,
                           books=books, num_of_books=book_num, fav_book_num=fav_book_num,
                           fav_books=fav_books, user=user, ub=ub, form=form, updateform=updateform)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = Users.query.filter_by(email=form.email.data).first()
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

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.confirm_password.data:
            hashed_password = generate_password_hash(
                form.password.data, method='sha256')
            if db.session.query(Users).filter_by(username=form.username.data).count() < 1:
                new_user = Users(username=form.username.data,
                                 email=form.email.data, password=hashed_password)
                try:
                    db.session.add(new_user)
                    flash("User  {} has been sucessfully created!".format(str(form.username.data)), "success")

                    return redirect("login")
                except:
                    db.session.rollback()
                finally:
                    db.session.commit()
            flash("username already exists", "warning")
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
            add_to_user_book = User_Books(book_id=new_book_created.id,
                                          book_summary=form.Summary.data, user_id=current_user.id)
            db.session.add(add_to_user_book)
            flash("new book added", "success")
            return redirect("dashboard")
        except:
            db.session.rollback()
        finally:
            db.session.commit()

    return render_template("book_new.html", form=form)


@app.route("/delete/<int:book_id>")
def delete(book_id):
    delete_book = User_Books.query.filter_by(book_id=book_id).first_or_404()
    if delete_book.user_id != current_user.id:
        abort(403)

    try:
        db.session.delete(delete_book)
        flash("Deleted successfully!", "success")
        
    except:
        db.session.rollback()
        return redirect("/dashboard")
    finally:
        db.session.commit()
        return redirect("/dashboard")

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    if request.method == "POST":
        try:
            update_book = Books.query.filter_by(id=id).first_or_404()
            update_book_summary = User_Books.query.filter_by(book_id=id).first_or_404()

            update_book.book_name = request.form['book_name']
            update_book.author = request.form['author']
            update_book.category = request.form['category']
            update_book_summary.book_summary = request.form['summary']
            update_book_summary.last_updated = datetime.datetime.now()
            flash("Book updated Successfully!", "success")
        except:
            db.session.rollback()
            flash("Couldn't update Book, Try again.", "warning")
        finally:
            db.session.commit()
    return redirect("/dashboard")



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)


"""
@app.route("/export")
def export():
    #data = zip(Book_titles,Book_prices)
    return render_template("export_books.html", data=("book", "idk"))
"""

"""
@app.route("/testform", methods=['GET', 'POST'])
def form():

    return render_template('test_forms.html')
"""