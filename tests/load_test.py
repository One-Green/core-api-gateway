import requests
from pprint import pprint
import ray
import random

ray.init()


@ray.remote
class Enclosure:
    api = 'http://192.168.0.21:8001/enclosure/'

    def post(self):
        _dict = {
            "enclosure_temperature": random.randint(15, 35),
            "enclosure_hygrometry": random.randint(40, 70),
            "enclosure_uv_index": "string",
            "enclosure_co2_ppm": random.randint(15, 90),
            "enclosure_cov_ppm": random.randint(15, 90)
        }
        return requests.post(self.api, json=_dict).json()

    def get(self):
        return requests.get(self.api).json()


@ray.remote
class AirHumidifier:
    api = 'http://192.168.0.21:8001/air-humidifier/'

    def post(self):
        _dict = {
            "water_level": random.randint(15, 90),
            "power_status": random.randint(0, 1)
        }
        return requests.post(self.api, json=_dict).json()

    def get(self):
        return requests.get(self.api).json()


@ray.remote
class Cooler:
    api = 'http://192.168.0.21:8001/cooler/'

    def post(self):
        _dict = {
            "air_in_temperature": random.randint(15, 90),
            "air_in_humidity": random.randint(15, 90),
            "air_out_temperature": random.randint(15, 90),
            "air_out_humidity": random.randint(15, 90),
            "cold_surface_temperature": random.randint(15, 90),
            "hot_surface_temperature": random.randint(15, 90),
            "power_status": random.randint(0, 1)
        }
        return requests.post(self.api, json=_dict).json()

    def get(self):
        return requests.get(self.api).json()


@ray.remote
class Heater:
    api = 'http://192.168.0.21:8001/heater/'

    def post(self):
        _dict = {
            "hot_surface_temperature": random.randint(15, 90),
            "air_in_temperature": random.randint(15, 90),
            "air_out_temperature": random.randint(15, 90),
            "power_status": random.randint(0, 1)
        }
        return requests.post(self.api, json=_dict).json()

    def get(self):
        return requests.get(self.api).json()


_cls = [
    Enclosure.remote(),
    AirHumidifier.remote(),
    Cooler.remote(),
    Heater.remote()
]

while True:
    future = []
    for _ in _cls:
        future.append(_.post.remote())
        future.append(_.get.remote())

    r = ray.get(future)
    for _ in r:
        pprint(_)
