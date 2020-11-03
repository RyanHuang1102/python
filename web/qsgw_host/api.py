from qsgw_token_api import *
def init_api(api):
    ## Global ##
    api.add_resource(qsgw_token_api, '/qsgw/api/v1/token')
