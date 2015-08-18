# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import resolve, reverse

from django.test.client import RequestFactory

from cms import api
from cms.middleware.toolbar import ToolbarMiddleware
from cms.test_utils.testcases import CMSTestCase
from cms.toolbar.toolbar import CMSToolbar
from cms.utils.conf import get_cms_setting
from cms.toolbar_pool import toolbar_pool

from ..cms_appconfig import ThingsConfig
from ..cms_toolbar import ThingsToolbar
from ..models import Thing

from . import ThingTestMixin


class TestToolbar(ThingTestMixin, CMSTestCase):

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.root_page = api.create_page(
            'root page',
            self.template,
            self.language,
            published=True
        )
        self.app_config = ThingsConfig.objects.create(
            namespace='things', app_title='Things')
        self.page = api.create_page(
            'Things',
            self.template,
            self.language,
            published=True,
            parent=self.root_page,
            apphook='ThingsApp',
            apphook_namespace=self.app_config.namespace
        )
        self.placeholder = self.page.placeholders.all()[0]
        self.request = self.get_request('en')

        for page in [self.root_page, self.page]:
            for language, _ in settings.LANGUAGES[1:]:
                api.create_title(language, page.get_slug(), page)
                page.publish(language)

        super(TestToolbar, self).setUp()

    def get_page_request(self, page, user, path=None, edit=False,
                         lang_code='en', disable=False):
        path = path or page and page.get_absolute_url()
        if edit:
            path += '?%s' % get_cms_setting('CMS_TOOLBAR_URL__EDIT_ON')
        request = RequestFactory().get(path)
        request.session = {}
        request.user = user
        request.LANGUAGE_CODE = lang_code
        if edit:
            request.GET = {'edit': None}
        else:
            request.GET = {'edit_off': None}
        if disable:
            request.GET[get_cms_setting('CMS_TOOLBAR_URL__DISABLE')] = None
        request.current_page = page
        mid = ToolbarMiddleware()
        mid.process_request(request)
        if hasattr(request, 'toolbar'):
            request.toolbar.populate()
        return request

    def get_toolbar(self, request):
        toolbar = CMSToolbar(request)
        toolbar.populate()
        toolbar.post_template_populate()
        return toolbar

    def test_get_on_delete_redirect_url(self):
        """
        Tests that the get_on_delete_redirect_url correctly returns the list
        view url.
        """
        url = self.thing1.get_absolute_url('en')
        request = self.get_page_request(self.page, self.get_superuser(), url)
        toolbar = self.get_toolbar(request)
        things_toolbar = ThingsToolbar(
            request, toolbar, True, 'things.ThingsConfig')
        redirect_url = things_toolbar.get_on_delete_redirect_url(self.thing1)
        list_view = reverse('{0}:thing-list'.format(self.app_config.namespace))
        self.assertTrue(list_view, redirect_url)

    def test_get_app_config(self):
        """
        Tests that the get_app_config() method returns the correct app_config.
        """
        url = self.thing1.get_absolute_url('en')
        request = self.get_page_request(self.page, self.get_superuser(), url)
        toolbar = self.get_toolbar(request)
        things_toolbar = ThingsToolbar(
            request, toolbar, True, 'things.ThingsConfig')
        self.assertEqual(
            things_toolbar.get_app_config(ThingsConfig), self.app_config)

        # Now check for a completely different config type
        self.assertIsNone(things_toolbar.get_app_config(Thing))

    def test_get_app_config_no_app_config(self):
        """
        Tests that the get_app_config() method returns None when there is no
        app_config on the request.
        """
        url = self.root_page.get_absolute_url('en')
        request = self.get_page_request(
            self.root_page, self.get_superuser(), url, edit=True)
        toolbar = self.get_toolbar(request)
        things_toolbar = ThingsToolbar(
            request, toolbar, False, None)
        # Now check for a completely different config type
        self.assertIsNone(things_toolbar.get_app_config(ThingsConfig))

    def test_toolbar_is_registered(self):
        """ Test that the toolbar is loading. """
        toolbars_items = toolbar_pool.get_toolbars()
        toolbars = [v for k, v in toolbars_items.items()]
        self.assertTrue(ThingsToolbar in toolbars)

    def test_watchmodels(self):
        """ Tests that the toolbar sets watch_models correctly. """
        self.assertTrue(Thing in toolbar_pool.get_watch_models())

    def test_populate_detail_view(self):
        url = self.thing1.get_absolute_url('en')
        request = self.get_page_request(
            self.page, self.get_superuser(), url, edit=True)
        request.resolver_match = resolve(request.path)
        toolbar = self.get_toolbar(request)
        things_menu = toolbar.get_menu('things-app')
        self.assertTrue(things_menu is not None)

        thing_menu_items = things_menu.get_items()
        thing_menu_item_names = [
            item.name for item in thing_menu_items if hasattr(item, 'name')]
        item_names = ['Configure addon ...', 'Thing list ...',
                      'Add new thing ...', 'Edit this thing ...',
                      'Delete this thing ...']

        for item_name in item_names:
            self.assertTrue(item_name in thing_menu_item_names)

    def test_populate_list_view(self):
        url = self.page.get_absolute_url('en')
        request = self.get_page_request(
            self.page, self.get_superuser(), url, edit=True)
        request.resolver_match = resolve(request.path)
        toolbar = self.get_toolbar(request)
        things_menu = toolbar.get_menu('things-app')
        self.assertTrue(things_menu is not None)

        thing_menu_items = things_menu.get_items()
        thing_menu_item_names = [
            item.name for item in thing_menu_items if hasattr(item, 'name')]
        item_names = ['Configure addon ...', 'Thing list ...',
                      'Add new thing ...']

        for item_name in item_names:
            self.assertTrue(item_name in thing_menu_item_names)
