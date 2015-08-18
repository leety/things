# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib import admin
from django.contrib.messages.middleware import MessageMiddleware
from django.test.client import RequestFactory

from cms import api
from cms.test_utils.testcases import CMSTestCase
from cms.utils.conf import get_cms_setting

from ..admin import ThingsConfigAdmin
from ..cms_appconfig import ThingsConfig

from . import ThingTestMixin, ThingsTransactionTestCase


class TestViews(ThingsTransactionTestCase):

    def test_get_config_fields(self):
        config_admin = ThingsConfigAdmin(ThingsConfig, admin.site)
        self.assertTrue(config_admin.get_config_fields(), ('app_title', ))


class TestAdminActions(ThingTestMixin, CMSTestCase):

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

        super(TestAdminActions, self).setUp()

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
        mid = MessageMiddleware()
        mid.process_request(request)
        return request
