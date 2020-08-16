import falcon
import orjson as json
from ..utils import get_now
from ..pk_rom.sprinkler import Sprinklers


class Registry:

    def on_post(self, req, resp):
        tag = req.media['tag']
        print(
            f"[{get_now()}] [INFO] "
            f"New Sprinkler with {tag=} "
            f"wan't to register ..."
        )
        if Sprinklers().is_tag_in_registry(tag):
            r = {"acknowledge": False}
            print(
                f"[{get_now()}] [WARNING] "
                f"This tag {tag=} is already in registry"
            )
        else:
            r = {"acknowledge": True}
            Sprinklers().add_tag_in_registry(tag)
            print(
                f"[{get_now()}] [OK] "
                f"New Sprinkler with {tag=} "
            )
        resp.body = json.dumps(r)
        resp.status = falcon.HTTP_200
