import requests
from pprint import pprint
import ray
import random


@ray.remote
class WaterPump:
    api = "http://192.168.0.21:8001/water-pump/"

    def post(self):
        _dict = {"water_level": random.randint(50, 70)}

        return requests.post(self.api, json=_dict).json()

    def get(self):
        return requests.get(self.api).json()


if __name__ == "__main__":

    ray.init()

    _cls = [
        WaterPump.remote(),
    ]

    while True:
        future = []
        for _ in _cls:
            future.append(_.post.remote())
            future.append(_.get.remote())

        r = ray.get(future)
        for _ in r:
            pprint(_)
