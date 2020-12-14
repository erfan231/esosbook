from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80)], render_kw={"placeholder": "Password"})
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
    Title = StringField("Title", validators=[InputRequired()])
    Author = StringField("Author")
    Category = StringField("Category")
    Summary = TextAreaField("Summary:", validators=[InputRequired()])
    Submit = SubmitField("Add book")
    add_to_fav = BooleanField('Move to favourite')


class ModalForm(FlaskForm):
    Submit = SubmitField("Update")
    add_to_fav = BooleanField('Move to favourite')
