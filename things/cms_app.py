# -*- coding: utf-8 -*

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from aldryn_apphooks_config.app_base import CMSConfigApp
from cms.apphook_pool import apphook_pool

from .cms_appconfig import ThingsConfig
# from .menu import ThingsMenu  # You shouldn't need this (read note below)


class ThingsApp(CMSConfigApp):
    """
    CMSConfigApp
    ------------
    This is provided by Aldryn Apphooks Config and provides support for "Spaces"
    or multiple apphooks. In particular it provides the methods: get_configs(),
    get_config(), and get_config_add_url().

    CMSConfigApp is a subclass of
    """
    app_name = 'ThingsApp'
    app_config = ThingsConfig
    name = _('Things')
    urls = ['things.urls']

    # NOTE: Only in very rare cases would you actually use menus here. We
    # should always give our users a choice of adding a menu or not and better
    # yet, different menu options to choose from.
    # menus = [ThingsMenu, ]

apphook_pool.register(ThingsApp)
