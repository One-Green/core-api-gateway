"""
MQTT based sprinklers controller

Purpose based on tag get confirmation from Redis
Use binary controller take action 0/1 to fill water
Subscribe to MQTT_SENSOR_TOPIC : excepted dict {"tag":<>, "soil_humidity":<> }
Publish to MQTT_CONTROLLER_TOPIC: published dict  {"tag":<>, "signal":<> }

Author: Shanmugathas Vigneswara
mail: shanmugathas.vigneswaran@outlook.fr
"""
import redis
import rom
from datetime import datetime
from settings import REDIS_HOST
from settings import REDIS_PORT
from core.pk_rom.sprinkler import Registry
from core.pk_rom.sprinkler import UpdatedAt
from core.pk_rom.sprinkler import Controller
import time

TIMEOUT: int = 1
BONJOUR: str = f'''
#########################################
## {REDIS_HOST=}
## {REDIS_PORT=}
#########################################
Sprinkler garbage collector
Purpose: 
- if not node message  > {TIMEOUT=} second, overwrite actuator signal to False  

'''

print(BONJOUR)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
rom.util.set_connection_settings(host=REDIS_HOST, port=REDIS_PORT, db=0)

while True:
    for _ in Registry.query.all():
        force = False
        tag = _.tag
        try:
            last_update = UpdatedAt.get_by(tag=tag).dt
            dt_now = datetime.utcnow()
            delta = (dt_now - last_update).seconds
            if delta > 1:
                print('[INFO] tag=' + tag + ' timeout detected, deactivate actuators')
                Controller.get_by(tag=tag).update(water_valve_signal=False).save()
        except AttributeError:
            force = True

        if force:
            try:
                print('[INFO] Can not get datetime for tag=' + tag + '  deactivate actuators')
                Controller.get_by(tag=tag).update(water_valve_signal=False).save()
            except AttributeError:
                pass
    time.sleep(1)


while True:
    try:
        UpdatedAt.get_by(tag="test").update(dt=datetime.utcnow()).save()
    except AttributeError:
        UpdatedAt(tag="test", dt=datetime.utcnow()).save()
