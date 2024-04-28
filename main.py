import os

from flask import Flask, redirect, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_uploads import configure_uploads, IMAGES, UploadSet

from werkzeug.utils import secure_filename

from web_project.data import db_session
from web_project.data.mappers import Mapper
from web_project.data.routes import Route
from web_project.forms.register import RegisterForm
from web_project.forms.login import LoginForm
from web_project.forms.add_post import PostForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOADED_IMAGES_DEST'] = 'uploads/images'

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    routes = db_sess.query(Route).all()
    return render_template("forum.html", routes=routes)


@login_manager.user_loader
def load_user(mapper_id):
    db_sess = db_session.create_session()
    return db_sess.query(Mapper).get(mapper_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        mapper = db_sess.query(Mapper).filter(Mapper.email == str(form.email.data)).first()
        if mapper and mapper.check_password(str(form.password.data)):
            login_user(mapper, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не одинаковые")
        db_sess = db_session.create_session()
        if db_sess.query(Mapper).filter(Mapper.email == str(form.email.data)).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой челик уже есть")
        mapper = Mapper(email=str(form.email.data), nickname=str(form.nickname.data), info=str(form.info.data))
        # f = form.profile_picture.data
        # mapper.profile_picture = f.read()
        mapper.set_password(str(form.password.data))
        db_sess.add(mapper)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_required
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        filename = images.save(form.image.data)
        return f'Filename: {filename}'
    return render_template('post.html', title='Регистрация', form=form)

def main():
    db_session.global_init('db/way_no_way.db')
    app.run()


if __name__ == '__main__':
    main()