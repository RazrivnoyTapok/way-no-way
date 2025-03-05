import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
import sqlalchemy.orm as orm
import datetime


class Route(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'routes'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, default=f'Route {id}')
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('mappers.id'))
    creation_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    private = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    image = sqlalchemy.Column(sqlalchemy.BLOB, nullable=False, default=open('static/img/map.png', mode='rb').read())
    ll = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='0,0')
    z = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='1')
    l = sqlalchemy.Column(sqlalchemy.String, default='map')
    info_r = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    info_m = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    mapper = orm.relationship('Mapper')
