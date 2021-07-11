import requests
from pprint import pprint
import random
import _pickle
import time

_list = _pickle.load(open("sign_list.pkl", "rb"))


class AirHumidifier:
    api = ""

    def post(self):
        _dict = {"air_in_humidity": 0, "air_out_humidity": 0}

        return requests.post(self.api, json=_dict).json()

    def post_sig(self):
        for _ in _list:
            _dict = {
                "air_in_humidity": _,
                "air_out_humidity": _,
            }

            pprint(requests.post(self.api, json=_dict).json())


if __name__ == "__main__":
    while True:
        AirHumidifier().post_sig()
        time.sleep(0.5)
