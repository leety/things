# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext as _, ungettext

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


class AdminActionHelper(object):
    def __init__(self, is_true, obj_name_plural, on_label, off_label):
        self.is_true = is_true
        self.obj_name_plural = obj_name_plural
        self.on_label = on_label
        self.off_label = off_label

    def get_state_label(self):
        return self.on_label if self.is_true else self.off_label

    def message_user(self, modeladmin, request, model, count, state):
        msg = ungettext(
            "%(count)d %(obj_name)s was set to %(state)s.",
            "%(count)d %(obj_name_plural)s were set to %(state)s.",
            count) % {
                'count': count,
                'obj_name': model._meta.verbose_name_raw,
                'obj_name_plural': self.obj_name_plural,
                'state': state}
        modeladmin.message_user(request, msg)

    @property
    def short_description(self):
        return _("Set selected {0} as {1}").format(
            self.obj_name_plural,
            self.get_state_label())

    @property
    def __name__(self):
        return "Set selected {0} as {1}".format(
            self.obj_name_plural,
            self.get_state_label())


class SetPublishedHelper(AdminActionHelper):

    def __call__(self, modeladmin, request, queryset):
        model = queryset.model
        count = queryset.update(is_published=self.is_true)
        state = self.get_state_label()
        self.message_user(modeladmin, request, model, count, state)


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
    list_display = ('name', 'is_published', )
    actions = (
        SetPublishedHelper(True, "things", "published", "unpublished"),
        SetPublishedHelper(False, "things", "published", "unpublished"),
    )
    # NOTE: TranslatableAdmin requires that ``fieldsets`` are defined in
    # ``_fieldsets`` (note the leading underscore).
    _fieldsets = (
        # Put translatable fields in the first section, as this is closely
        # associated with the language tabs in the UI.
        (None, {
            'fields': (
                ('name', 'slug'),
            )
        }),
        # Put non-translated fields in subsequent sections.
        (_('Advanced'), {
            'classes': ('collapse',),
            'fields': (
                'is_published',
            )
        }),
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
