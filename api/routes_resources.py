from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.routes import Route
from api.routes_resources_parse import parser


def abort_if_news_not_found(route_id):
    session = db_session.create_session()
    route = session.query(Route).get(route_id)
    if not route:
        abort(404, message=f"Route {route_id} not found")


class RouteResource(Resource):
    def get(self, route_id: int):
        abort_if_news_not_found(route_id)
        session = db_session.create_session()
        route = session.query(Route).get(route_id)
        return jsonify({'route': route.to_dict(only=('name', 'description', 'author', 'creation_date',
                                                     'private', 'll', 'z', 'l', 'info_r', 'info_m'))})

    def delete(self, route_id):
        abort_if_news_not_found(route_id)
        session = db_session.create_session()
        route = session.query(Route).get(route_id)
        session.delete(route)
        session.commit()
        return jsonify({'success': 'OK'})


class RouteListResource(Resource):
    def get(self):
        session = db_session.create_session()
        routes = session.query(Route).all()
        return jsonify({'routes': [r.to_dict(only=('name', 'description', 'author', 'creation_date', 'private',
                                                   'll', 'z', 'l', 'info_r', 'info_m')) for r in routes]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        route = Route(name=args['name'],
                      description=args['description'],
                      author=args['author'],
                      private=args['private'],
                      ll=args['ll'],
                      z=args['z'],
                      l=args['l'],
                      info_r=args['info_r'],
                      info_m=args['info_m'])
        session.add(route)
        session.commit()
        return jsonify({'id': route.id})
