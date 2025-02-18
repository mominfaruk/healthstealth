from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.enums.user_role import UserRole


def get_sentinel_user():
    return get_user_model().objects.get_or_create(
        email='deleted@mail.com',
        username='deleted@mail.com',
        user_mode=UserRole.TechAdmin.value,
        is_deleted=True
    )[0]


class Activity(models.Model):
    is_deleted = models.BooleanField(_('Delete status'), default=False, null=False, blank=False)
    added_by = models.ForeignKey(
        verbose_name=_('Add by'),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name='%(app_label)s_%(class)s_added_by',
        null=True,
        blank=False
    )
    changed_by = models.ForeignKey(
        verbose_name=_('Change by'),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name='%(app_label)s_%(class)s_changed_by',
        null=True,
        blank=True
    )
    deleted_by = models.ForeignKey(
        verbose_name=_('Delete by'),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name='%(app_label)s_%(class)s_delete_by',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True
