# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from menus.menu_pool import menu_pool

from ..menu import ThingsMenu

from . import ThingsTransactionTestCase


class TestMenu(ThingsTransactionTestCase):

    def test_get_nodes(self):
        request = self.get_page_request(None, self.user, '/en/')

        try:
            # CMS 3.5+
            renderer = menu_pool.get_renderer(request)
            menu = ThingsMenu(renderer=renderer)
        except AttributeError:
            # CMS < 3.5
            menu = ThingsMenu()

        nodes = menu.get_nodes(request)
        self.thing1.set_current_language('en')
        self.thing2.set_current_language('en')
        self.assertEqualItems(
            [menuitem.title for menuitem in nodes],
            [self.thing1.name, self.thing2.name],
        )

        # Test that the DE version has 2 categories and their questions that
        # they are shown in German.
        request = self.get_page_request(None, self.user, '/de/')

        try:
            # CMS 3.5+
            renderer = menu_pool.get_renderer(request)
            menu = ThingsMenu(renderer=renderer)
        except AttributeError:
            # CMS < 3.5
            menu = ThingsMenu()

        nodes = menu.get_nodes(request)
        self.thing1.set_current_language('de')
        self.thing2.set_current_language('de')
        self.assertEqualItems(
            [menuitem.title for menuitem in nodes],
            [self.thing1.name, self.thing2.name]
        )
