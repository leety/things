# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import override, ugettext_lazy as _

from aldryn_translation_tools.models import (
    TranslatedAutoSlugifyMixin,
    TranslationHelperMixin,
)
from cms.utils.i18n import get_current_language, get_default_language

from parler.models import TranslatableModel, TranslatedFields

from .managers import ThingManager
from .cms_appconfig import ThingsConfig


class Thing(TranslatedAutoSlugifyMixin, TranslationHelperMixin,
            TranslatableModel):
    """
    TranslatableModel
    -----------------
    This is provided by Parler and provides the heavy lifting for translatable
    models.

    TranslationHelperMixin
    ----------------------
    This is provided by Aldryn Translation Tools. At time of this writing, this
    simply provides the method ``known_translation_getter`` on the object. This
    works a bit like Parler's ``safe_translation_getter``, but returns a tuple
    («value», «language»). The «language» is the language that «value» is
    translated in.

    TranslatedAutoSlugifyMixin
    --------------------------
    This is provided by Aldryn Translation Tools and provides automatic
    slugification from the name field, in a manner that respects translations.
    The mixin has many options so be sure to review the source for details.
    """
    slug_source_field_name = 'name'

    translations = TranslatedFields(
        name=models.CharField(
            _('name'), max_length=255, blank=False, default=''),
        slug=models.SlugField(
            _('slug'), max_length=255, blank=True, default=''),
        meta={'unique_together': (('language_code', 'slug'), )},
    )

    # Notice that boolean fields are named 'is_*' this is a convention we wish
    # to uphold.
    is_published = models.BooleanField(_('is published?'), default=False)

    # Not every model should have a link to the app config, but core models
    # probably should.
    app_config = models.ForeignKey(ThingsConfig, verbose_name=_('app_config'))

    objects = ThingManager()

    class Meta:
        verbose_name = _('thing')
        verbose_name_plural = _('things')

    def get_absolute_url(self, language=None):
        """
        Given a thing object, return its URL. If language fallbacks are
        configured, then this should respect them. However, we should **never**
        try to do anything with the ``redirect_on_fallback`` settings in CMS
        and Parler here. That responsibility lies in the views.

        Essentially, if a caller provides an object that has a valid **active**
        language, then this will return a valid URL, not NoReverseMatch.

        However, if the caller attempts to request the URL, but the object does
        not have an **active** language translation, this may indeed, return a
        NoReverseMatch.

        :param language: The *desired* language.
        :return: The URL in the desired language, or a fallback, if configured.
        """
        if not language:
            language = get_current_language() or get_default_language()
        slug, language = self.known_translation_getter(
            'slug', None, language_code=language)
        kwargs = {'slug': slug}

        with override(language):
            return reverse('things:thing-detail', kwargs=kwargs)
