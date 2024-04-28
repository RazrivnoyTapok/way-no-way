from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Пароль, ещё разок', validators=[DataRequired()])
    nickname = StringField('Никнейм', validators=[DataRequired()])
    info = TextAreaField("О себе")
    profile_picture = FileField('Аватарка')
    submit = SubmitField('Зарегистрироваться')