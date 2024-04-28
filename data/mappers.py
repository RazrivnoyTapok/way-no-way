import sqlalchemy
from web_project.data.db_session import SqlAlchemyBase
import sqlalchemy.orm as orm
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_login import UserMixin


class Mapper(SqlAlchemyBase, UserMixin):
    __tablename__ = 'mappers'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=f'Mapper {id}')
    info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    profile_picture = sqlalchemy.Column(sqlalchemy.BLOB, nullable=False,
                                        default=open('other/Без имени.png', mode='rb').read())
    join_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    routes = orm.relationship("Route", back_populates='mapper')


    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)