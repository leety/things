# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _, get_language_from_request

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse

from aldryn_apphooks_config.utils import get_app_instance
from parler.models import TranslatableModel

from .models import Thing
from .cms_appconfig import ThingsConfig


# TODO: Candidate to move to Aldryn Translation Tools
def get_obj_from_request(model, request,
                         pk_url_kwarg='pk',
                         slug_url_kwarg='slug',
                         slug_field='slug'):
    """
    Given a model and the request, try to extract and return an object
    from an available 'pk' or 'slug', or return None.

    Note that no checking is done that the obj's kwargs really are for objects
    matching the provided model (how would it?) so use only where appropriate.
    """
    language = get_language_from_request(request, check_path=True)
    kwargs = request.resolver_match.kwargs
    mgr = model.objects
    if pk_url_kwarg in kwargs:
        return mgr.filter(pk=kwargs[pk_url_kwarg]).first()
    elif slug_url_kwarg in kwargs:
        # If the model is translatable, and the given slug is a translated
        # field, then find it the Parler way.
        filter_kwargs = {slug_field: kwargs[slug_url_kwarg]}
        translated_fields = model._parler_meta.get_translated_fields()
        if (issubclass(model, TranslatableModel) and
                slug_url_kwarg in translated_fields):
            return mgr.active_translations(language, **filter_kwargs).first()
        else:
            # OK, do it the normal way.
            return mgr.filter(**filter_kwargs).first()
    else:
        return None


# TODO: Candidate for moving to Aldryn Translation Tools
def get_admin_url(action, action_args=[], **url_args):
    """
    Convenience method for constructing admin-urls with GET parameters.

    :param action:      The admin url key for use in reverse. E.g.,
                        'things_edit_thing'
    :param action_args: The url args for the reverse. E.g., [thing.pk, ]
    :param url_args:    A dict of key/value pairs for GET parameters. E.g.,
                        {'language': 'en', }.
    :return: The complete admin url
    """
    base_url = admin_reverse(action, args=action_args)
    # Converts [{key: value}, …] => ["key=value", …]
    # We sort the dict into a sequence of tuples for predictability. Testing
    # reveals that different versions of Python/Django behave differently.
    url_args_tuple = sorted([(k, v) for k, v in url_args.items()])
    params = urlencode(url_args_tuple)
    if params:
        return "?".join([base_url, params])
    else:
        return base_url


@toolbar_pool.register
class ThingsToolbar(CMSToolbar):
    # watch_models must be a list, not a tuple
    # see https://github.com/divio/django-cms/issues/4135
    watch_models = [Thing, ]
    supported_apps = ('things', )

    def get_on_delete_redirect_url(self, thing):
        """
        NOTE: The redirect functionality won't really work unless django CMS is
        version 3.0.15 or greater or 3.1.3 or greater. However, do provide this
        anyway so that it will work properly then.

        :param thing: Thing we will be deleting
        :return: Url to the thing list view.
        """
        url = reverse('{0}:thing-list'.format(thing.app_config.namespace))
        return url

    def get_app_config(self, config_class=None):
        try:
            __, config = get_app_instance(self.request)
            if not isinstance(config, config_class):
                # This is not the app_hook you are looking for.
                return None
        except ImproperlyConfigured:
            # There is no app_hook at all.
            return None

        return config

    def populate(self):
        config = self.get_app_config(ThingsConfig)
        if not config:
            # Do nothing if there is no NewsBlog app_config to work with
            return
        user = getattr(self.request, 'user', None)
        try:
            view_name = self.request.resolver_match.view_name
        except AttributeError:
            view_name = None

        if user and view_name:
            language = get_language_from_request(self.request, check_path=True)

            # If we're on an thing detail page, then get the thing
            if view_name == '{0}:thing-detail'.format(config.namespace):
                thing = get_obj_from_request(Thing, self.request)
            else:
                thing = None

            menu = self.toolbar.get_or_create_menu('things-app',
                                                   config.get_app_title())

            change_config_perm = user.has_perm('things.change_thingsconfig')

            add_thing_perm = user.has_perm('things.add_thing')
            change_thing_perm = user.has_perm('things.change_thing')
            delete_thing_perm = user.has_perm('things.delete_thing')
            thing_perms = [add_thing_perm, change_thing_perm,
                           delete_thing_perm, ]

            if change_config_perm:
                url_args = {}
                if language:
                    url_args = {'language': language, }
                url = get_admin_url('things_thingsconfig_change',
                                    [config.pk, ], **url_args)
                menu.add_modal_item(_('Configure addon'), url=url)

            if change_config_perm and any(thing_perms):
                menu.add_break()

            if change_thing_perm:
                url_args = {}
                if config:
                    url_args = {'app_config__id__exact': config.pk}
                url = get_admin_url('things_thing_changelist',
                                    **url_args)
                menu.add_sideframe_item(_('Thing list'), url=url)

            if add_thing_perm:
                url_args = {'app_config': config.pk, 'owner': user.pk, }
                if language:
                    url_args.update({'language': language, })
                url = get_admin_url('things_thing_add', **url_args)
                menu.add_modal_item(_('Add new thing'), url=url)

            if change_thing_perm and thing:
                url_args = {}
                if language:
                    url_args = {'language': language, }
                url = get_admin_url('things_thing_change',
                                    [thing.pk, ], **url_args)
                menu.add_modal_item(_('Edit this thing'), url=url, active=True)

            if delete_thing_perm and thing:
                redirect_url = self.get_on_delete_redirect_url(thing)
                url = get_admin_url('things_thing_delete',
                                    [thing.pk, ])
                menu.add_modal_item(_('Delete this thing'), url=url,
                                    on_close=redirect_url)
