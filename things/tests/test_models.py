# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import override
try:
    from django.utils.translation import force_text
except:
    from django.utils.translation import force_unicode as force_text

from ..models import Thing
from . import ThingsTransactionTestCase


class TestModels(ThingsTransactionTestCase):

    def test_slug(self):
        # Ensure that identical slugs under the same language are not created
        with override('en'):
            thing = Thing.objects.create(app_config=self.app_config,
                                         name='Sample', is_published=True)
            self.assertEquals('sample', thing.slug)

            thing1 = Thing.objects.create(app_config=self.app_config,
                                          name='Sample', is_published=True)
            self.assertEquals('sample-1', thing1.slug)

        # Ensure that identical slugs under differing languages is OK.
        with override('de'):
            thing = Thing.objects.create(app_config=self.app_config,
                                         name='Sample')
            self.assertEquals('sample', thing.slug)

    def test_add_people_app(self):
        """
        Test that the app_hook works and that get_absolute_url() on things work
        as expected.
        """
        with override('en'):
            url = self.thing1.get_absolute_url('en')
            self.assertEquals('/en/things/thing-one/', url)

            url = self.thing1.get_absolute_url()
            self.assertEquals('/en/things/thing-one/', url)

            url = self.thing1.get_absolute_url('de')
            self.assertEquals('/de/things/objekt-eins/', url)

    def test_app_config_get_app_title(self):
        with override('en'):
            self.assertEquals('Things',
                              force_text(self.app_config.get_app_title()))
