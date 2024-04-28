from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание')
    private = BooleanField('Скрытый')
    image = FileField('Изображение на карте')
    text = FileField('Файл маршрута')
    submit = SubmitField('Опубликовать')