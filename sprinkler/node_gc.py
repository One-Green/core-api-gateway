"""
Sprinkler node garbage collector

Purpose:

1/ Cut off water_valve_signal , if Node is down MQTT message.
   If no message from Sprinkler Node Controller not updated (sprinkler.models.Controller.updated_at)
   Use django orm to filter and update water_valve_signal=False if updated_at datetime
   is larger than datetime now - timedelta(second=TIMEOUT)



Author: Shanmugathas Vigneswaran
mail: shanmugathas.vigneswaran@outlook.fr
"""
import os
import sys
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
sys.path.insert(0, os.path.abspath(".."))
django.setup()

from sprinkler.models import Controller
from project.settings import SPRINKLER_GC_CUTOFF_TIMEOUT

BONJOUR: str = f'''
#########################################
Sprinkler garbage collector
Purpose: 
- if not node message  > {SPRINKLER_GC_CUTOFF_TIMEOUT=} second, overwrite actuator signal to False
#########################################

Garbage collector started
'''

print(BONJOUR)
while True:
    Controller.objects.\
        filter(updated_at__lte=timezone.now()-timedelta(seconds=SPRINKLER_GC_CUTOFF_TIMEOUT))\
        .update(water_valve_signal=False)
