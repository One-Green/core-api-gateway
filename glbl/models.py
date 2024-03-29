from django.db import models
from glbl.helpers import timezone_validator


class Config(models.Model):
    site_tag = models.CharField(unique=True, null=False, blank=False, max_length=200)
    address = models.CharField(unique=True, null=True, blank=True, max_length=200)
    timezone = models.TextField(
        unique=True, null=False, blank=False, validators=[timezone_validator]
    )
