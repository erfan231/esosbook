from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from database_org import *
from forms import LoginForm, RegisterForm, PostForm, UpdateForm, RequestPasswordResetForm, ResetPasswordForm
from sqlalchemy.exc import IntegrityError
import datetime
from flask_mail import Mail, Message
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'new_erfan'  # os.environ.get("Secret_Key")
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
app.config["MAIL_USERNAME"] = "erfanmahmoodicvc@gmail.com"  # os.environ.get("EMAIL_USER")
app.config["MAIL_PASSWORD"] = "erfanmahqw1"  # os.environ.get("EMAIL_PASSWORD")

mail = Mail(app)


host = "192.168.20.25"
port = 5000


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
    updateform = UpdateForm() # make the move to fav from general books
    user_books = User_Books.query.filter_by(user_id=current_user.id).all()
    ub = user_books

    user = Users.query.filter_by(username=str(current_user.username)).first()
    books = user.user_books
    book_num = books.count()

    fav_books = user.user_fav_books  # get the fav books using table relationships between user and fav_books
    fav_book_num = fav_books.count()

    # adding books modal
    if form.validate_on_submit():
        # deciding weather to add to fav books or normal books
        book_id = db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).first() #for later use
        if form.add_to_fav.data == False:

            if db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() < 1:
                try:
                    new_book_created = Books(book_name=form.Title.data, author=form.Author.data,
                                             category=form.Category.data, owner=current_user.id)

                    db.session.add(new_book_created)
                    db.session.commit()

                    add_to_user_book = User_Books(user_id=current_user.id,book_id=new_book_created.id,
                                                  book_summary=form.Summary.data, time_added=datetime.datetime.now(), last_updated=datetime.datetime.now())
                    db.session.add(add_to_user_book)
                    flash("{} has been added successfully to your book collection".format(form.Title.data), "success")
                    return redirect("dashboard")

                except:
                    db.session.rollback()
                    flash("An error occured, try again.", "warning")
                finally:
                    db.session.commit()
            elif db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() >= 1 and db.session.query(User_Books).filter_by(book_id=book_id.id, user_id=current_user.id).count() < 1:

                add_to_user_book = User_Books(book_id=book_id.id,
                                              book_summary=form.Summary.data, user_id=current_user.id, time_added=datetime.datetime.now(), last_updated=datetime.datetime.now())
                db.session.add(add_to_user_book)
                flash("{} has been added successfully to your book collection".format(form.Title.data), "success")
                return redirect("dashboard")
            elif db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() >= 1 and db.session.query(User_Books).filter_by(book_id=book_id.id, user_id=current_user.id).count() >= 1:
                flash("Book already in your collection", "success")

        # add to fav books
        #flash("boolean working", "success")
        if form.add_to_fav.data == True:
            if db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() < 1:
                    try:
                        new_book_created = Books(book_name=form.Title.data, author=form.Author.data,
                                                category=form.Category.data, owner=current_user.id)

                        db.session.add(new_book_created)
                        db.session.commit()

                        add_to_user_book = User_fav_books(user_id=current_user.id,book_id=new_book_created.id,
                                                    book_summary=form.Summary.data, time_added=datetime.datetime.now(), last_updated=datetime.datetime.now())
                        db.session.add(add_to_user_book)
                        flash("{} has been added successfully to your book collection".format(form.Title.data), "success")
                        return redirect("dashboard")

                    except:
                        db.session.rollback()
                        flash("An error occured, try again.", "warning")
                    finally:
                        db.session.commit()
            elif db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() >= 1 and db.session.query(User_fav_books).filter_by(book_id=book_id.id, user_id=current_user.id).count() < 1:

                add_to_user_fav_book = User_fav_books(book_id=book_id.id,
                                            book_summary=form.Summary.data, user_id=current_user.id, time_added=datetime.datetime.now(), last_updated=datetime.datetime.now())
                db.session.add(add_to_user_fav_book)
                flash("{} has been added successfully to your book collection".format(form.Title.data), "success")
                return redirect("dashboard")
            elif db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() >= 1 and db.session.query(User_fav_books).filter_by(book_id=book_id.id, user_id=current_user.id).count() >= 1:
                flash("Book already in your collection", "success")
        """
        if db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() < 1:
            try:
                create_new_book = Books(book_name=form.Title.data, author=form.Author.data,
                                         category=form.Category.data, owner=current_user.id)
                db.session.add(create_new_book)
                db.session.commit()
                add_to_user_fav_book = User_fav_books(user_id=current_user.id,book_id=create_new_book.id,book_summary=form.Summary.data, time_added=datetime.datetime.now(), last_updated=datetime.datetime.now())
                db.session.add(add_to_user_fav_book)
                flash("{} has been added successfully to your favourite book collection".format(form.Title.data), "success")
                return redirect("dashboard")
            except:
                db.session.rollback()
                flash("An error occured, try again.", "warning")
            finally:
                db.session.commit()

        elif db.session.query(Books).filter_by(book_name=form.Title.data, owner=current_user.id).count() >= 1:
            add_to_user_fav_book = User_fav_books(book_id=book_id.id,
                                                  book_summary=form.Summary.data, user_id=current_user.id, time_added=datetime.datetime.now(), last_updated=datetime.datetime.now())
            db.session.add(add_to_user_fav_book)
            flash("{} has been added successfully to your favourite book collection".format(form.Title.data), "success")
            return redirect("dashboard")
            """

    return render_template('dashboard.html', name=current_user.username,
                           books=books, num_of_books=book_num, fav_book_num=fav_book_num,
                           fav_books=fav_books, user=user, ub=ub, form=form, updateform=updateform)


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
                flash("Invalid Credential, Try again", "warning")
        else:
            flash("User don't exists, Please Sign Up", "warning")

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


@app.route("/delete/<int:book_id>")
@login_required
def delete(book_id):
    delete_book = db.session.query(User_Books).filter_by(book_id=book_id).first_or_404()
    #delete_book = User_Books.query.filter_by(book_id=book_id).first_or_404()
    if delete_book.user_id != current_user.id:
        abort(403)

    db.session.delete(delete_book)
    db.session.commit()
    flash("Deleted successfully!", "success")

    # db.session.rollback()
    #flash("couldn't delete book", "warning")
    db.session.commit()
    return redirect(url_for("dashboard"))


@app.route("/delete_fav_book/<int:book_id>")
@login_required
def delete_fav_book(book_id):
    delete_book = db.session.query(User_fav_books).filter_by(book_id=book_id).first_or_404()
    #delete_book = User_Books.query.filter_by(book_id=book_id).first_or_404()
    if delete_book.user_id != current_user.id:
        abort(403)

    db.session.delete(delete_book)
    db.session.commit()
    flash("Deleted successfully!", "success")

    # db.session.rollback()
    #flash("couldn't delete book", "warning")
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/update/<int:id>", methods=["POST"])
@login_required
def update(id):
    if request.method == "POST":
        try:
            #update_book = Books.query.filter_by(id=id).first_or_404()
            #update_book_summary = User_Books.query.filter_by(book_id=id).first_or_404()
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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender="noreply@EsosBook.com",
                  recipients=[user.email])
    msg.body = f"""To reset your password visit the following link:
{url_for('reset_password', token=token, _external=True)}


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


"""
@app.route("/export")
def export():
    #data = zip(Book_titles,Book_prices)
    return render_template("export_books.html", data=("book", "idk"))
"""






"""   ADD NEW BOOK THROUGH A PAGE

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
            flash("Book added successfully!", "success")
            return redirect("dashboard")
        except:
            db.session.rollback()
        finally:
            db.session.commit()

    return render_template("book_new.html", form=form)


"""
