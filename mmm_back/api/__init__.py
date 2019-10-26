from flask_restplus import Api


from mmm_back.api.mmm import ns_mmm
from mmm_back.api.conserts import ns_conserts
from mmm_back.api.plsync import ns_plsync


api = Api(
    title='mmm_API',
    version='0.1',
    description='Shifty API',
)

api.add_namespace(ns_mmm)
api.add_namespace(ns_conserts)
api.add_namespace(ns_plsync)
