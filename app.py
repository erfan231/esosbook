import datetime
import os

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from forms import LoginForm, PostForm, RegisterForm, RequestPasswordResetForm, ResetPasswordForm, UpdateForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
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
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASSWORD")

mail = Mail(app)


host = "192.168.20.25"
port = 5000

import database #to avoid import circualr import error

User_Books = database.User_Books
Books = database.Books
Users = database.Users
User_fav_books = database.User_fav_books
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html', current_user_is_authenticated=current_user.is_authenticated)


@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    form = PostForm()
    updateform = UpdateForm()  # make the move to fav from general books
    user_books = User_Books.query.filter_by(user_id=current_user.id).all()
    ub = user_books
    user_fav_books = User_fav_books.query.filter_by(user_id=current_user.id).all()
    ub_fav_books = user_fav_books

    user = Users.query.filter_by(username=str(current_user.username)).first()
    books = user.user_books
    book_num = books.count()

    fav_books = user.user_fav_books  # get the fav books using table relationships between user and fav_books
    fav_book_num = fav_books.count()

    # adding books
    if form.validate_on_submit():
        # deciding weather to add to fav books or normal books
        if form.add_to_fav.data == False:

            if db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() <= 0:
                try:
                    new_book_created = Books(book_name=form.Title.data, author=form.Author.data,
                                             category=form.Category.data, owner=current_user.id)

                    db.session.add(new_book_created)
                    db.session.commit()
                    add_to_user_book = User_Books(user_id=current_user.id, book_id=new_book_created.id,
                                                  book_summary=form.Summary.data, time_added=datetime.datetime.now(), last_updated=datetime.datetime.now())
                    db.session.add(add_to_user_book)
                    flash("{} has been added successfully to your book collection".format(form.Title.data), "success")
                    return redirect("dashboard")

                except:
                    db.session.rollback()
                    flash("An error occured, try again.", "warning")
                finally:
                    db.session.commit()

            elif db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() >= 1 and db.session.query(User_fav_books).filter_by(book_id=db.session.query(Books).filter_by(book_name=form.Title.data).first().id, user_id=current_user.id).count() >= 1:
                flash("Book already exists in favourite books table", "info")

            # books in Books table but not in user books table
            elif db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() >= 1 and db.session.query(User_Books).filter_by(book_id=db.session.query(Books).filter_by(book_name=form.Title.data).first().id,
                                                                                                                                                             user_id=current_user.id).count() <= 0:

                add_to_user_book = User_Books(user_id=current_user.id, book_id=db.session.query(Books).filter_by(book_name=form.Title.data).first().id,
                                              book_summary=form.Summary.data, time_added=datetime.datetime.now(), last_updated=datetime.datetime.now())
                db.session.add(add_to_user_book)
                db.session.commit()
                flash("{} has been added successfully to your book collection".format(form.Title.data), "success")
                return redirect("dashboard")
            # Book exists in both table
            elif db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() >= 1 and db.session.query(User_Books).filter_by(book_id=db.session.query(Books).filter_by(book_name=form.Title.data).first().id, user_id=current_user.id).count() >= 1:
                flash("Book already in your collection", "info")

        # add to fav books
        if form.add_to_fav.data == True:
            if db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() <= 0:
                try:
                    new_book_created = Books(book_name=form.Title.data, author=form.Author.data,
                                             category=form.Category.data, owner=current_user.id)

                    db.session.add(new_book_created)
                    db.session.commit()

                    add_to_user_book = User_fav_books(user_id=current_user.id, book_id=new_book_created.id,
                                                      book_summary=form.Summary.data, time_added=datetime.datetime.now(), last_updated=datetime.datetime.now())
                    db.session.add(add_to_user_book)
                    flash("{} has been added successfully to your book collection".format(form.Title.data), "success")
                    return redirect("dashboard")

                except:
                    db.session.rollback()
                    flash("An error occured, try again.", "warning")
                finally:
                    db.session.commit()
            elif db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() >= 1 and db.session.query(User_Books).filter_by(book_id=db.session.query(Books).filter_by(book_name=form.Title.data).first().id, user_id=current_user.id).count() >= 1:
                flash("Book already exists in normal books table", "info")

            elif db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() >= 1 and db.session.query(User_fav_books).filter_by(book_id=db.session.query(Books).filter_by(book_name=form.Title.data).first().id,
                                                                                                                                                                 user_id=current_user.id).count() <= 0:

                add_to_user_book = User_fav_books(user_id=current_user.id, book_id=db.session.query(Books).filter_by(book_name=form.Title.data).first().id,
                                                  book_summary=form.Summary.data, time_added=datetime.datetime.now(), last_updated=datetime.datetime.now())
                db.session.add(add_to_user_book)
                db.session.commit()
                flash("{} has been added successfully to your book collection".format(form.Title.data), "success")
                return redirect("dashboard")

            # Book exists in both table
            elif db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() >= 1 and db.session.query(User_fav_books).filter_by(book_id=db.session.query(Books).filter_by(book_name=form.Title.data).first().id, user_id=current_user.id).count() >= 1:
                flash("Book already exists in your collection", "info")
            # Book exists in User_Books table

    return render_template('dashboard.html', name=current_user.username,
                           books=books, num_of_books=book_num, fav_book_num=fav_book_num,
                           fav_books=fav_books, user=user, ub=ub, ub_fav_books=ub_fav_books, form=form, updateform=updateform)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("dashboard")
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
                flash("Invalid credential, Try again", "warning")
        else:
            flash("Sorry, but we can't find an account with this email address. Please try again or create a new account.", "warning")

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect("dashboard")

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.confirm_password.data:
            hashed_password = generate_password_hash(
                form.password.data, method='sha256')
            if db.session.query(Users).filter_by(email=form.email.data).count() < 1:
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
            flash("An account with that Email address already exists, Try loggin in", "warning")
        flash("Password doesn't match", "warning")

    return render_template('signup.html', form=form)


@app.route("/user")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/delete/<int:book_id>")
@login_required
def delete(book_id):
    delete_book = db.session.query(User_Books).filter_by(book_id=book_id).first_or_404()
    if delete_book.user_id != current_user.id:
        abort(403)
    try:
        db.session.delete(delete_book)
        flash("Deleted successfully!", "success")
    except:
        db.session.rollback()
        flash("couldn't delete book", "warning")
    finally:
        db.session.commit()
    return redirect(url_for("dashboard"))


@app.route("/delete-fav-book/<int:book_id>")
@login_required
def delete_fav_book(book_id):
    delete_book = db.session.query(User_fav_books).filter_by(book_id=book_id).first_or_404()
    if delete_book.user_id != current_user.id:
        abort(403)
    try:
        db.session.delete(delete_book)
        flash("Deleted successfully!", "success")
    except:
        db.session.rollback()
        flash("couldn't delete book", "warning")

    finally:
        db.session.commit()
        return redirect(url_for("dashboard"))


@app.route("/update/<int:id>", methods=["POST"])
@login_required
def update(id):
    if request.method == "POST":
        try:
            db.session.query(Books).filter_by(id=id).update({"book_name": request.form["book_name"],
                                                             "author": request.form["author"],
                                                             "category": request.form["category"]})
            db.session.query(User_Books).filter_by(book_id=id).update({"book_summary": request.form["summary"],
                                                                       "last_updated": datetime.datetime.now()})
            flash("Book updated Successfully!", "success")
        except:
            db.session.rollback()
            flash("Couldn't update Book, Try again.", "warning")
        finally:
            db.session.commit()
    return redirect("/dashboard")


@app.route("/update-fav-book/<int:id>", methods=["POST"])
@login_required
def update_fav_book(id):
    if request.method == "POST":
        try:
            db.session.query(Books).filter_by(id=id).update({"book_name": request.form["book_name"],
                                                             "author": request.form["author"],
                                                             "category": request.form["category"]})
            db.session.query(User_fav_books).filter_by(book_id=id).update({"book_summary": request.form["summary"],
                                                                           "last_updated": datetime.datetime.now()})
            flash("Book updated Successfully!", "success")
        except:
            db.session.rollback()
            flash("Couldn't update Book, Try again.", "warning")
        finally:
            db.session.commit()
    return redirect("/dashboard")


@app.route("/remove-from-fav-group/<int:id>", methods=["POST", "GET"])
@login_required
def remove_from_fav_group(id):
    if request.method == "GET":
        remove_book = db.session.query(User_fav_books).filter_by(book_id=id, user_id=current_user.id).first()
        move_book = User_Books(user_id=current_user.id, book_id=remove_book.book_id, book_summary=remove_book.book_summary,
                               time_added=remove_book.time_added, last_updated=remove_book.last_updated)

        db.session.add(move_book)
        db.session.commit()
        db.session.delete(remove_book)
        db.session.commit()
        flash("transfer successful!", "success")

    return redirect("/dashboard")


@app.route("/add-to-fav-group/<int:id>", methods=["POST", "GET"])
@login_required
def add_to_fav_group(id):
    if request.method == "GET":
        remove_book = db.session.query(User_Books).filter_by(book_id=id, user_id=current_user.id).first()
        move_book = User_fav_books(user_id=current_user.id, book_id=remove_book.book_id, book_summary=remove_book.book_summary,
                                   time_added=remove_book.time_added, last_updated=remove_book.last_updated)

        db.session.add(move_book)
        db.session.commit()
        db.session.delete(remove_book)
        db.session.commit()
        flash("transfer successful!", "success")
    return redirect("/dashboard")


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender="noreply@EsosBook.com",
                  recipients=[user.email])
    msg.body = f"""To reset your password visit the following link:
{url_for('reset_password', token=token, _external=True)}
The link will expire in 30 minutes.


If you did not make this request then simply ignore this email and no changes will be made.
 """

    mail.send(msg)


@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect("dasboard")

    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", "info")
        return redirect("/login")

    return render_template("reset_password_request.html", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    global hashed_password

    form = ResetPasswordForm()
    if current_user.is_authenticated:
        return redirect("dasboard")
    user = Users.verify_reset_token(token)
    if user is None:
        flash("Invalid or expired token", "warning")
        return redirect("/reset_password_request")

    if form.validate_on_submit():
        if form.Password.data == form.Confirm_Password.data:
            try:
                hashed_password = generate_password_hash(
                    form.Password.data, method='sha256')

                user.password = hashed_password
                db.session.query(Users).filter_by(id=user.id).update({"password": hashed_password})
                flash("{} Your password has been updated!".format(user.username), "success")
                return redirect("/login")
            except:
                flash("an error occured", "warning")
            finally:
                db.session.commit()
        flash("Password don't match", "warning")

    return render_template("reset_password.html", form=form)


@app.errorhandler(404)
def http_error_handler(error):
    return render_template("404.html"), 404


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/testform", methods=['GET', 'POST'])
def form():

    return render_template('test_forms.html')


if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)
