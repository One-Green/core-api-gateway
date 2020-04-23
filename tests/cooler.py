import requests
from pprint import pprint
import random
import _pickle
import time

_list = _pickle.load(open("sign_list.pkl", "rb"))


class Cooler:
    api = "http://127.0.0.1:8001/cooler/"

    def post(self):
        _dict = {
            "air_in_temperature": random.randint(20, 50),
            "air_out_temperature": random.randint(20, 50),
            "air_in_humidity": random.randint(20, 50),
            "air_out_humidity": random.randint(20, 50),
            "heater_temperature": random.randint(20, 50),
        }

        return requests.post(self.api, json=_dict).json()

    def post_sig(self):
        for _ in _list:
            _dict = {
                "air_in_temperature": _,
                "air_out_temperature": _,
                "air_in_humidity": _,
                "air_out_humidity": _,
            }

            pprint(requests.post(self.api, json=_dict).json())


if __name__ == "__main__":
    while True:
        Cooler().post_sig()
        time.sleep(0.5)
