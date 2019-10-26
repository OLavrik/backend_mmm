from .req_parsers import get_concerts
from flask import Response
from flask_restplus import Namespace, Resource, fields
import requests

ns = Namespace('conserts', description='Api for proxying requests to concerts database')




@ns.route('/')
class Concerts(Resource):
    @ns.response(200, 'Success')
    @ns.expect(get_concerts)
    def get(self):
        args = get_concerts.parse_args()
        query_params = {'session': 123, 'title': args['artist']}
        storage_response = requests.get('https://api.cultserv.ru/v4/events/list', params=query_params)
        return storage_response.json(), 200


