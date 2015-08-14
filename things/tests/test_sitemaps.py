# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..sitemaps import ThingsSitemap

from . import ThingsTransactionTestCase


class TestSitemaps(ThingsTransactionTestCase):

    def test_sitemap_items(self):
        sitemap = ThingsSitemap()
        self.assertEqualItems(
            [item.pk for item in sitemap.items()],
            [self.thing1.pk, self.thing2.pk]
        )

    def test_sitemap_locations(self):
        # First let's try EN
        sitemap = ThingsSitemap('en')
        self.assertEqualItems(
            [sitemap.location(item) for item in sitemap.items()],
            [
                self.thing1.get_absolute_url('en'),
                self.thing2.get_absolute_url('en')
            ]
        )
        # OK, now let's do DE
        sitemap = ThingsSitemap('de')
        self.assertEqualItems(
            [sitemap.location(item) for item in sitemap.items()],
            [
                self.thing1.get_absolute_url('de'),
                self.thing2.get_absolute_url('de')
            ]
        )
