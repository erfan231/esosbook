from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import Email, InputRequired, Length

import database


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField('password', validators=[
                             InputRequired(), Length(max=80)], render_kw={"placeholder": "Password"})
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)], render_kw={"placeholder": "Email"})

    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=6, max=80)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired()], render_kw={"placeholder": "Confirm Password"})


class PostForm(FlaskForm):
    Title = StringField("Title", validators=[InputRequired()], render_kw={"placeholder": "Title of the Book"})
    Author = StringField("Author", render_kw={"placeholder": "Author of the Book"})
    Category = StringField("Category", render_kw={"placeholder": "E.g Fiction"})
    Summary = TextAreaField("Summary:", validators=[InputRequired()], render_kw={"placeholder": "Notes"})
    Submit = SubmitField("Add book")
    add_to_fav = BooleanField('Move to favourite')


class UpdateForm(FlaskForm):
    Title = StringField("Title", validators=[InputRequired()], render_kw={"placeholder": "Title of the Book"})
    Author = StringField("Author", render_kw={"placeholder": "Author of the Book"})
    Category = StringField("Category", render_kw={"placeholder": "E.g Fiction"})
    Summary = TextAreaField("Summary:", validators=[InputRequired()], render_kw={"placeholder": "Notes"})
    Submit = SubmitField("Update")
    move_to_fav = BooleanField('Move to favourite', default=False)
    remove_from_fav = BooleanField("Remove from Favorite", default=False)


class RequestPasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)], render_kw={"placeholder": "Email"})
    Submit = SubmitField("Confirm")

    def validate_email(self, email):
        user = database.Users.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. You must register first")


class ResetPasswordForm(FlaskForm):
    Password = PasswordField('New Password', validators=[
                             InputRequired(), Length(min=6, max=80)], render_kw={"placeholder": "New Password"})
    Confirm_Password = PasswordField(
        "Confirm Password", validators=[InputRequired()], render_kw={"placeholder": "Confirm Password"})

    Submit = SubmitField("Reset Password")
