# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_apphooks_config.managers.base import ManagerMixin, QuerySetMixin
from parler.managers import TranslatableManager, TranslatableQuerySet


class ThingQuerySet(QuerySetMixin, TranslatableQuerySet):
    """
    TranslatableQuerySet
    --------------------
    This is provided by Django Parler and provides transparent access to the
    translated fields as well as the queryset filters to support the language(),
    translated(), and active_translations() methods.

    QuerySetMixin
    -------------
    This is provided by Aldryn Apphooks Config and it provides support for a
    .namespace() query filter.
    """
    def published(self):
        """
        Returns articles that are published AND have a publishing_date that
        has actually passed.
        """
        return self.filter(is_published=True)


class ThingManager(ManagerMixin, TranslatableManager):
    """
    TranslatableManager
    -------------------
    This is provided by Django Parler and provides default use of the above-
    defined Queryset class as well as the commonly used methods: language(),
    translated(), and active_translations()

    ManagerMixin
    ------------
    This is provided by Aldryn Apphooks Config and provides the namespace()
    method.
    """
    queryset_class = ThingQuerySet

    def get_queryset(self):
        qs = ThingQuerySet(self.model, using=self.db)
        return qs

    def published(self):
        return self.get_queryset().published()
