import falcon
import calendar
from datetime import datetime


class UTCTimeStamp:

    def on_get(self, req, resp):
        resp.body = str(calendar.timegm(datetime.now().utctimetuple()))
        resp.status = falcon.HTTP_200
