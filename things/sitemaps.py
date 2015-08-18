# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_translation_tools.sitemaps import I18NSitemap

from .models import Thing


class ThingsSitemap(I18NSitemap):
    """
    I18NSitemap
    -----------
    This is provided by Aldryn Translation Tools and augments the normal,
    django.contrib.sitemap with the ability to accept a language-code in the
    constructor, and use the same when getting an items location.

    NOTE: It is important that when you implement Sitemap.items() the queryset
    will limit the objects to only those available in the language specified in
    self.language.
    """
    changefreq = "weekly"
    priority = 0.75

    def items(self):
        return Thing.objects.published().translated(self.language).all()
