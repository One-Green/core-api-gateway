import falcon
import rom
from core.gateway import sprinkler
from settings import (
    REDIS_HOST,
    REDIS_PORT
)


rom.util.set_connection_settings(host=REDIS_HOST, port=REDIS_PORT, db=0)
api = application = falcon.API()
api.add_route('/sprinkler/registry', sprinkler.Registry())
