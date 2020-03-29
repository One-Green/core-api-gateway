import requests
from pprint import pprint
import ray
import random


@ray.remote
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
            "soil_hygrometry": random.randint(15, 90)
        }
        return requests.post(
            self.api,
            json=_dict
        ).json()

    def get(self):
        _dict = {
            "tag": self.tag
        }
        return requests.get(
            self.api,
            json=_dict
        ).json()


if __name__ == '__main__':

    ray.init()

    _cls = [
        Sprinkler.remote(),
    ]

    while True:
        future = []
        for _ in _cls:
            future.append(_.post.remote())
            future.append(_.get.remote())

        r = ray.get(future)
        for _ in r:
            pprint(_)
