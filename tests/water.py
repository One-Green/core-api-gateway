import requests
from pprint import pprint
import random
import _pickle
import time

_list = _pickle.load(open("sign_list.pkl", "rb"))


class Water:
    api = "http://192.168.0.20:8001/water/"

    def post_sig(self):
        for _ in _list:
            _dict = {
                "level": _,
            }

            pprint(requests.post(self.api, json=_dict).json())


if __name__ == "__main__":
    while True:
        Water().post_sig()
        time.sleep(0.5)
