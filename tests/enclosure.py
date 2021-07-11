import requests
from pprint import pprint
import random
import _pickle
import time

_list = _pickle.load(open("sign_list.pkl", "rb"))


class Enclosure:
    api = ""

    def post(self):
        _dict = {
            {
                "temperature": random.randint(20, 50),
                "humidity": random.randint(20, 50),
                "uv_index": "string",
                "co2_ppm": random.randint(20, 50),
                "cov_ppm": random.randint(20, 50),
            }
        }

        return requests.post(self.api, json=_dict).json()

    def post_sig(self):
        for _ in _list:
            _dict = {
                "temperature": random.randint(20, 50),
                "humidity": random.randint(20, 50),
                "uv_index": "string",
                "co2_ppm": random.randint(20, 50),
                "cov_ppm": random.randint(20, 50),
            }

            pprint(requests.post(self.api, json=_dict).json())


if __name__ == "__main__":
    while True:
        Enclosure().post_sig()
        time.sleep(0.5)
