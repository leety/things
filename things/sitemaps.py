# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import NoReverseMatch
from django.contrib.sitemaps import Sitemap
from django.utils import translation

from .models import Thing


class I18NSitemap(Sitemap):

    def __init__(self, language=None):
        if language:
            self.language = language
        else:
            self.language = settings.LANGUAGES[0][0]

    def location(self, item):
        with translation.override(self.language):
            try:
                return item.get_absolute_url()
            except NoReverseMatch:  # pragma: no cover
                # Note, if we did our job right in items(), this
                # shouldn't happen at all.
                return ''


class ThingsSitemap(I18NSitemap):
    changefreq = "weekly"
    priority = 0.75

    def items(self):
        return Thing.objects.published().translated(self.language).all()
