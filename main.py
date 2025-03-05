import os

import flask
from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_uploads import configure_uploads, IMAGES, TEXT, UploadSet, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, StringField, TextAreaField, BooleanField, EmailField, PasswordField
from wtforms.validators import DataRequired
from flask_restful import Api

from requests import get, post, delete

from data import db_session
from data.mappers import Mapper
from data.routes import Route
from forms.register import RegisterForm
from forms.login import LoginForm
from api.routes_resources import RouteResource, RouteListResource

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_lyceum_secret_key'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads/images')
app.config['UPLOADED_TEXTS_DEST'] = os.path.join(basedir, 'uploads/texts')

api = Api(app)
api.add_resource(RouteResource, '/api/routes/<int:route_id>')
api.add_resource(RouteListResource, '/api/routes')

photos = UploadSet('photos', IMAGES)
texts = UploadSet('texts', TEXT)
configure_uploads(app, [photos, texts])
patch_request_class(app)

login_manager = LoginManager()
login_manager.init_app(app)


class UploadForm(FlaskForm):
    name = StringField(validators=[DataRequired('Нет значения!')])
    desc = TextAreaField(validators=[DataRequired('Нет значения!')])
    priv = BooleanField()
    photo = FileField(validators=[FileAllowed(photos, 'Только картинки!'), FileRequired('Нет файла!')])
    text = FileField(validators=[FileAllowed(texts, 'Только текст!'), FileRequired('Нет файла!')])
    submit = SubmitField('Запостить')


class SearchPostForm(FlaskForm):
    prompt = StringField('Ввести текст для поиска')
    submit = SubmitField('Искать')


class DownloadForm(FlaskForm):
    dl_text = BooleanField('Загрузить файл')
    dl_image = BooleanField('Загрузить картинку')
    submit = SubmitField('Загрузить')


class SettingsForm(FlaskForm):
    pass  # Настройки сайта пока не придуманы


class RedactAccountForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    email_new = EmailField('Почта (новая)')
    password_new = PasswordField('Пароль (новый)')
    password_new_again = PasswordField('Пароль (новый), ещё разок')
    submit = SubmitField('Сохранить изменения')


class RedactProfileForm(FlaskForm):
    nickname = StringField('Никнейм')
    info = TextAreaField("О себе")
    profile_picture = FileField('Аватарка', validators=[FileAllowed(photos, 'Только картинки!')])
    submit = SubmitField('Сохранить изменения')


def test_api(r, rl):
    print(r.get(1).json)
    print(rl.get().json)


@app.route("/", methods=['GET', 'POST'])
@app.route("/<int:page>")
def index(page=0):
    delete_cash()
    form = SearchPostForm()
    db_sess = db_session.create_session()
    file_url = []
    routes = db_sess.query(Route).order_by(-Route.id).filter(Route.id >= page * 10, Route.id < page * 10 + 10).all()
    if request.method == "POST":
        routes = db_sess.query(Route).filter(Route.name.like(f'%{form.prompt.data}%')).limit(10).all()
    for i in range(len(routes)):
        r = routes[i]
        with open(f'static/img/static{i}.png', mode='wb') as f:
            f.write(r.image)
            file_url.append(f'static/img/static{i}.png')
    return render_template("forum.html", page=page, routes=routes, file_url=file_url, form=form)


@login_manager.user_loader
def load_user(mapper_id):
    db_sess = db_session.create_session()
    return db_sess.query(Mapper).get(mapper_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    delete_cash()
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        mapper = db_sess.query(Mapper).filter(Mapper.email == form.email.data).first()
        if mapper and mapper.check_password(form.password.data):
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
    delete_cash()
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не одинаковые")
        db_sess = db_session.create_session()
        if db_sess.query(Mapper).filter(Mapper.email == str(form.email.data)).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        mapper = Mapper(email=form.email.data, nickname=form.nickname.data, info=form.info.data)
        if form.profile_picture.data:
            mapper.profile_picture = form.profile_picture.data
        mapper.set_password(str(form.password.data))
        db_sess.add(mapper)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    delete_cash()
    form = UploadForm()
    if form.validate_on_submit():
        image_name = photos.save(form.photo.data)
        text_name = texts.save(form.text.data)
        db_sess = db_session.create_session()

        with open(os.path.join(basedir, f'uploads/images/{image_name}'), mode='rb') as img:
            image_bytes = img.read()

        with open(os.path.join(basedir, f'uploads/texts/{text_name}'), mode='rt', encoding='utf-8') as f:
            dt = list(map(lambda x: x.strip('\n'), f.readlines()))
            ll, z, l = dt[0], dt[1], dt[2]
            r = '&'.join(dt[3:6])
            m = '&'.join(dt[6:17])
            route = Route(name=form.name.data,
                          description=form.desc.data,
                          author=current_user.id,
                          private=form.priv.data,
                          image=image_bytes,
                          ll=ll, z=z, l=l,
                          info_r=r, info_m=m)
            db_sess.add(route)
            db_sess.commit()

        os.remove(f'uploads/images/{image_name}')
        os.remove(f'uploads/texts/{text_name}')
    return render_template('post.html', form=form)


@app.route('/post_view/<int:post_id>', methods=['GET', 'POST'])
def post_view(post_id: int):
    delete_cash()
    form = DownloadForm()
    db_sess = db_session.create_session()
    route = db_sess.query(Route).filter(Route.id == post_id).first()
    if route.private is True and current_user != route.mapper:
        return "Sorry! We can't show this post, it's private."
    if request.method == 'GET':
        with open(f'static/pfp/pfp{post_id}.png', mode='wb') as f:
            f.write(route.mapper.profile_picture)
        with open(f'static/img/static0.png', mode='wb') as f:
            f.write(route.image)
        return render_template('view.html', route=route, form=form,
                               pfp=url_for('static', filename=f'pfp/pfp{post_id}.png'),
                               img=url_for('static', filename='img/static0.png'))
    elif request.method == 'POST':
        if not (form.dl_text.data or form.dl_image.data):
            return redirect(f'/post_view/{post_id}')
        else:
            if form.dl_image.data:
                return flask.send_from_directory(basedir, 'static/img/static0.png')
            if form.dl_text.data:
                with open(os.path.join(basedir, 'static/text/text0.txt'), mode='wt', encoding='utf-8') as f:
                    dt = [route.ll, route.z, route.l, *route.info_r.split('&'), *route.info_m.split('&')]
                    f.writelines(dt)
                return flask.send_from_directory(basedir, 'static/text/text0.txt')
            return redirect(f'/post_view/{post_id}')


@app.route('/profile_view/<int:profile_id>')
def view_profile(profile_id: int):
    delete_cash()
    db_sess = db_session.create_session()
    mapper = db_sess.query(Mapper).filter(Mapper.id == profile_id).first()
    with open(f'static/pfp/pfp{profile_id}.png', mode='wb') as f:
        f.write(mapper.profile_picture)
    return render_template('profile.html', mapper=mapper,
                           pfp=url_for('static', filename=f'pfp/pfp{profile_id}.png'))


@login_required
@app.route('/user_cabinet')
def user_cabinet():
    delete_cash()
    form = SettingsForm()
    mapper = current_user
    with open('static/pfp/pfp0.png', mode='wb') as f:
        f.write(mapper.profile_picture)
    return render_template('user_cab_blocks.html', mapper=mapper, form=form,
                           pfp=url_for('static', filename=f'pfp/pfp0.png'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/application')
def application():
    return flask.send_from_directory(basedir, 'Way-No-Way-app.zip')


@login_required
@app.route('/redact_profile', methods=['GET', 'POST'])
def redact():
    delete_cash()
    form = RedactProfileForm()
    db_sess = db_session.create_session()
    mapper = db_sess.query(Mapper).filter(Mapper.id == current_user.id).first()
    if form.validate_on_submit():
        mapper.nickname = form.nickname.data if form.nickname.data != '' else mapper.nickname
        mapper.info = form.info.data if form.info.data != '' else mapper.info
        if form.profile_picture.data:
            image_name = photos.save(form.profile_picture.data)
            with open(os.path.join(basedir, f'uploads/images/{image_name}'), mode='rb') as img:
                image_bytes = img.read()
            mapper.profile_picture = image_bytes
        db_sess.commit()
    return render_template('redact.html', form=form)


def delete_cash():
    for file in os.listdir(os.path.join(basedir, 'static/pfp')):
        if file != 'Без имени.png':
            os.remove(f'static/pfp/{file}')
    for file in os.listdir(os.path.join(basedir, 'static/img')):
        if file != 'map.png':
            os.remove(f'static/img/{file}')
    for file in os.listdir(os.path.join(basedir, 'static/text')):
        os.remove(f'static/text/{file}')


def main():
    db_session.global_init('db/way_no_way.db')
    # with app.app_context():
    #     r = RouteResource()
    #     rl = RouteListResource()
    #     test_api(r, rl)
    app.run()


if __name__ == '__main__':
    main()
