# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext as _

from aldryn_apphooks_config.admin import BaseAppHookConfig
from aldryn_reversion.admin import VersionedPlaceholderAdminMixin
from aldryn_translation_tools.admin import AllTranslationsMixin
from cms.admin.placeholderadmin import (
    PlaceholderAdminMixin,
    FrontendEditableAdminMixin
)
from parler.admin import TranslatableAdmin

from .cms_appconfig import ThingsConfig
from .models import Thing


class ThingAdmin(AllTranslationsMixin, FrontendEditableAdminMixin,
                 VersionedPlaceholderAdminMixin, TranslatableAdmin):
    """
    TranslatableAdmin
    -----------------
    This is the base Admin class provided by Parler. It provides almost perfect
    compatibility with the normal way of declaring an admin class. There are
    some exceptions though, as noted inline below.

    VersionedPlaceholderAdminMixin
    ------------------------------
    This is provided by Aldryn Reversion and provides nearly all the
    revision-magic in a single mixin.

    PlaceholderAdminMixin
    ---------------------
    This is already an ancestor of ``VersionedPlaceholderAdmin``, so, if your
    model is already using ``VersionedPlaceholderAdminMixin`` there is no need
    to also add ``PlaceholderAdminMixin``. However, if your project is not
    revisioned, and you do have ``PlaceholderField`` fields defined, then you
    must add this mixin to your model.

    FrontendEditableAdminMixin
    --------------------------
    If you plan to use {% render_model … %} (or a variant), in your templates,
    you should add ``FrontendEditableAdminMixin`` to your Admin form.

    AllTranslationsMixin
    --------------------
    The ``AllTranslationsMixin`` will add a set of click-able language "tags"
    in the last column of the changelist-obj that are hyper-linked to the
    object's change-form in the indicated language. They also serve to visually
    communicate (via color) which translations are available. If you wish to
    reposition this to another column (not recommended), simply place the field
    "all_translations" wherever you like in the ``list_display`` tuple.
    """
    list_display = ('name', )

    # NOTE: TranslatableAdmin requires that ``fieldsets`` are defined in
    # ``_fieldsets`` (note the leading underscore).
    _fieldsets = (
        # Put translatable fields in the first section, as this is closely
        # associated with the language tabs in the UI.
        (None, {'fields': (
            ('name', 'slug'),
        )}),
        # Put non-translated fields in subsequent sections.
        (_('Advanced'), {
            'classes': ('collapse',),
            'fields': (
            )
        })
    )

admin.site.register(Thing, ThingAdmin)


class ThingsConfigAdmin(AllTranslationsMixin, PlaceholderAdminMixin,
                       BaseAppHookConfig, TranslatableAdmin):
    """
    BaseAppHookConfig
    -----------------
    This is actually a mixin and should be used on TranslatableAdmin (or just
    ModelAdmin, if your project isn't translatable). This is provided by
    Aldryn Apphooks Config.
    """
    def get_config_fields(self):
        return ('app_title', )

admin.site.register(ThingsConfig, ThingsConfigAdmin)
