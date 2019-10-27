import os
from flask import Flask
from flask_cors import CORS
from mmm_back.api import api
import logging

# stream_handler = logging.StreamHandler(stream=sys.stdout)
# stream_handler.setLevel(logging.DEBUG)
# stream_handler.setFormatter(logging.Formatter(
#     '[%(asctime)s] %(name)s %(levelname)s in %(module)s: %(message)s'
# ))
# logging.getLogger().addHandler(stream_handler)
# logging.getLogger().setLevel(logging.DEBUG)

UPLOAD_FOLDER = '/var/www/'

def create_app(config=None):
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['CORS_HEADERS'] = 'Content-Type, DNT'
    CORS(app, resources={r"/*": {"origins": "*"}})    # load default configuration

    # load environment configuration
    if 'WEBSITE_CONF' in os.environ:
        app.config.from_envvar('WEBSITE_CONF')

    # load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

    setup_app(app)

    return app


def setup_app(app):
    # Create tables if they do not exist already
    # @app.before_first_request
    # def create_tables():
    #     db.create_all()
    #
    # db.init_app(app)
    # config_oauth(app)
    api.init_app(app)


# POSTGRES = {
#     'user': 'mmm_back',
#     'pw': '1234',
#     'db': 'mmm_back',
#     'host': '185.91.53.50',
#     'port': '5432',
# }
#
app = create_app({
    'SECRET_KEY': 'secret',
    'OAUTH2_REFRESH_TOKEN_GENERATOR': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
})


if __name__ == '__main__':
    app.run()