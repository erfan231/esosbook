from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
#import request
from database import app, db, Users, Books
from sqlalchemy.exc import IntegrityError
from flask import request

db.create_all()



host = "10.254.25.210"
port = 5000

bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=15)],render_kw={"placeholder": "Username"})
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80)],render_kw={"placeholder": "Password"})
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)],render_kw={"placeholder": "Email"})
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=6, max=80)],render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired()],render_kw={"placeholder": "Confirm Password"})


@app.route('/')
def index():
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
            flash("Invalid Credential, Try again", "warning")

        flash("user don't exists", "warning")

        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    login_form = LoginForm()
    pass_not = None #for later use

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

                return render_template('login.html', form=login_form)
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
            except IntegrityError as error:
                flash("User already exists. Please login instead", "warning")
        pass_not = "password don't match"
        flash(pass_not, "warning")

    return render_template('signup.html', form=form, flash=flash, pass_not = pass_not)




@app.route('/dashboard')
@login_required
def dashboard():
    #default values
    books = ""
    
    try:
        user = Users.query.filter_by(username=str(current_user.username)).first()
        books = user.user_books
        book_num = books.count()

        fav_books = user.usr_fav_books
        fav_book_num = fav_books.count()

    except:
        flash("An error occured when trying to get your books", "danger")
    return render_template('dashboard.html', name=current_user.username, books=books, num_of_books=book_num,fav_book_num=fav_book_num,fav_books=fav_books)


@app.route("/export")
def export():
    #data = zip(Book_titles,Book_prices)
    return render_template("export_books.html", data=("book", "idk"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/testform", methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Do Something':
           return "DO something worked"
        elif request.form['submit_button'] == 'Do Something Else':
            pass # do something else
    
    elif request.method == 'GET':
        return render_template('test_forms.html', form=form)

@app.route("/user")
@login_required
def profile():
    return render_template("profile.html")

if __name__ == '__main__':
    app.run(debug=True,host=host,port=port)
