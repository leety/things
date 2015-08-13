# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from ..admin import ThingsConfigAdmin
from ..cms_appconfig import ThingsConfig

from . import ThingsTransactionTestCase


class TestViews(ThingsTransactionTestCase):

    def test_get_config_fields(self):
        config_admin = ThingsConfigAdmin(ThingsConfig, admin.site)
        self.assertTrue(config_admin.get_config_fields(), ('app_title', ))
