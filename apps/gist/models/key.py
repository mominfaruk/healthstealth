import re
import uuid

from django.db import models
from django.db.models import Manager
from django.utils.translation import gettext_lazy as _



class Key(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
