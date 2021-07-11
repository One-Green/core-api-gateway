import json
import random
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883, 60)

while True:
    _dict = {"value": True, "_dict": {"test": random.randint(0, 100)}}
    client.publish("tests/tag-1", json.dumps(_dict))
