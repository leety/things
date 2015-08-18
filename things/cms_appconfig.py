# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from aldryn_apphooks_config.models import AppHookConfig
# from cms.models.fields import PlaceholderField
from parler.models import TranslatableModel, TranslatedFields


class ThingsConfig(TranslatableModel, AppHookConfig):
    """
    Adds some translatable, per-app-instance fields.
    """

    translations = TranslatedFields(
        app_title=models.CharField(
            _('application title'), max_length=234, blank=True, default=''),
    )

    def get_app_title(self):
        return getattr(self, 'app_title', _('untitled'))
