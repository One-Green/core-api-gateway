import time
import requests
from pprint import pprint
import random
import _pickle

_list = _pickle.load(open("sign_list.pkl", "rb"))


class Sprinkler:
    api = "http://127.0.0.1:31801/api-v1/sprinkler/"

    @property
    def tag(self):
        return random.choice(["tag-1", "tag-2", "tag-3", "tag-4", "tag-5"])

    def post(self):
        _dict = {"tag": self.tag, "soil_humidity": random.randint(50, 60)}
        return requests.post(self.api, json=_dict).json()

    def post_sig(self):
        for _ in _list:
            _dict = {"tag": self.tag, "soil_humidity": _}

            pprint(requests.post(self.api, json=_dict).json())


if __name__ == "__main__":
    while True:
        Sprinkler().post_sig()
        time.sleep(1)
