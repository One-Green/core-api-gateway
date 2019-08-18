import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.join(os.path.dirname('__file__')))))
django.setup()
from django.contrib.auth.models import User

User.objects.create_superuser('plant', 'change@me.com', 'keeper')
