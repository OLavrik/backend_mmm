from flask_restplus import Namespace, Resource, fields

ns = Namespace('mmm', description='Item related operations')


req_get_item_model = ns.model('Get mmm', {
    'find_str': fields.String,
    'user_id': fields.String,
})


@ns.route('/')
class Hello(Resource):
    @ns.response(200, 'Alive')
    def get(self):
        return {'status': 'alive'}, 200


