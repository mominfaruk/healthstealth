from django.db import models
from django.utils.translation import gettext_lazy as _

class TimeLog(models.Model):
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True, blank=True, null=True)
    deleted_at = models.DateTimeField(_("Deleted at"), blank=True, null=True)

    class Meta:
        abstract = True