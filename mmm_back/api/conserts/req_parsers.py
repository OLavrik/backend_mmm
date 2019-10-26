from flask_restplus import reqparse

get_concerts = reqparse.RequestParser()
get_concerts.add_argument('artist', help='Artist name for finding')
