from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str)
parser.add_argument('description', required=True, type=str)
parser.add_argument('author', required=True, type=int)
parser.add_argument('private', required=True, type=bool)
parser.add_argument('ll', required=True, type=str)
parser.add_argument('z', required=True, type=str)
parser.add_argument('l', required=True, type=str)
parser.add_argument('info_r', required=True, type=str)
parser.add_argument('info_m', required=True, type=str)