import time
import requests
from pprint import pprint
import random
import _pickle

_list = _pickle.load(open('sign_list.pkl', 'rb'))


class Sprinkler:
    api = 'http://192.168.0.21:8001/sprinkler-valve/'

    @property
    def tag(self):
        return random.choice(
            [
                'tag-1',
                'tag-2',
                'tag-3',
                'tag-4',
                'tag-5'
            ]
        )

    def post(self):
        _dict = {
            "tag": self.tag,
            "soil_humidity": random.randint(50, 60)
        }
        return requests.post(
            self.api,
            json=_dict
        ).json()

    def post_sig(self):
        for _ in _list:
            print(_)
            _dict = {
                "tag": self.tag,
                "soil_humidity": _
            }

            requests.post(
                self.api,
                json=_dict
            )



if __name__ == '__main__':
    while True:
        pprint(Sprinkler().post_sig())
