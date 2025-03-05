from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.mappers import Mapper
from api.mappers_resources_parse import parser


def abort_if_news_not_found(mapper_id):
    session = db_session.create_session()
    mapper = session.query(Mapper).get(mapper_id)
    if not mapper:
        abort(404, message=f"Mapper {mapper_id} not found")


class MapperResource(Resource):
    def get(self, mapper_id: int):
        abort_if_news_not_found(mapper_id)
        session = db_session.create_session()
        mapper = session.query(Mapper).get(mapper_id)
        return jsonify({'mapper': mapper.to_dict(only=('nickname', 'info', 'join_date'))})

    def delete(self, mapper_id):
        abort_if_news_not_found(mapper_id)
        session = db_session.create_session()
        mapper = session.query(Mapper).get(mapper_id)
        session.delete(mapper)
        session.commit()
        return jsonify({'success': 'OK'})


class MapperListResource(Resource):
    def get(self):
        session = db_session.create_session()
        mappers = session.query(Mapper).all()
        return jsonify({'mappers': [r.to_dict(only=('nickname', 'info', 'join_date')) for r in mappers]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        mapper = Mapper(nickname=args['nickname'],
                        email=args['email'],
                        hashed_password=args['hashed_password'],
                        info=args['info'])
        session.add(mapper)
        session.commit()
        return jsonify({'id': mapper.id})
