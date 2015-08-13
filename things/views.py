# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import (
    Http404,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
)
from django.views.generic import DetailView, ListView

from menus.utils import set_language_changer
from parler.views import TranslatableSlugMixin, ViewUrlMixin

from aldryn_apphooks_config.mixins import AppConfigMixin

from .models import Thing


# TODO: Candidate for moving into Aldryn Translation Tools
class LanguageChangerMixin(object):
    """
    Simple mixin that adds django CMS language changer support to the obj.
    This should only be used on detail views or other single-object views.
    """
    def get(self, request, *args, **kwargs):
        if not hasattr(self, 'object'):
            self.object = self.get_object()
        set_language_changer(request, self.object.get_absolute_url)
        return super(LanguageChangerMixin, self).get(request, *args, **kwargs)


# TODO: Candidate for moving into Aldryn Translation Tools
class AllowPKsTooMixin(object):
    def get_object(self, queryset=None):
        """
        Bypass TranslatableSlugMixin if we are using PKs. You would only use
        this if you have a obj that supports accessing the object by pk or
        by its translatable slug.

        NOTE: This should only be used on DetailViews and this mixin MUST be
        placed to the left of TranslatableSlugMixin. In fact, for best results,
        declare your obj like this:

            MyView(…, AllowPKsTooMixin, TranslatableSlugMixin, DetailView):
        """
        if self.pk_url_kwarg in self.kwargs:
            return super(DetailView, self).get_object(queryset)

        # OK, just let Parler have its way with it.
        return super(AllowPKsTooMixin, self).get_object(queryset)


# TODO: Candidate for moving into Aldryn Apphooks Config
class AppConfigViewUrlMixin(ViewUrlMixin):
    """
    Overrides Django Parler's own ViewUrlMixin to work properly with projects
    that support application namespaces. This particular implementation will
    prefix any value set in «self.view_url_name» with the application namespace
    if one is present. Override as necessary.
    """
    view_url_name = None

    def get_view_url_name(self):
        if not self.view_url_name:
            raise ImproperlyConfigured(
                "Missing `view_url_name` attribute on {0}".format(
                    self.__class__.__name__))

        if hasattr(self, 'namespace'):
            view_url_name = "{0}:{1}".format(self.namespace, self.view_url_name)
        else:
            view_url_name = self.view_url_name

        return view_url_name

    def get_view_url(self):
        view_url_name = self.get_view_url_name()
        return reverse(view_url_name, args=self.args, kwargs=self.kwargs)


# TODO: Candidate for moving into Aldryn Translation Tools
class CanonicalUrlMixin(AppConfigViewUrlMixin):
    """
    Provides configurable control over how non-canonical URLs to views are
    handled. A obj can specify by setting 'non_canonical_url_response_type' to
    one of 200, 301, 302 or 404. By default, handling will be to temporarily
    redirect to the canonical URL.
    """
    non_canonical_url_response_type = 302

    def get_non_canonical_url_response_type(self):
        response_type = getattr(self, "non_canonical_url_response_type", None)
        if response_type and response_type in [200, 301, 302, 404]:
            return response_type
        else:
            return 302

    def get(self, request, *args, **kwargs):
        """
        On GET, if the URL used is not the correct one, handle according to
        preferences by either:
            Allowing (200),
            Temprarily redirecting (302),
            Permanently redirecting (301) or
            Failing (404).
        """
        self.object = self.get_object()
        url = self.object.get_absolute_url()
        response_type = self.get_non_canonical_url_response_type()
        if (response_type == 200 or request.path == url):
            return super(CanonicalUrlMixin, self).get(
                request, *args, **kwargs)
        if response_type == 302:
            return HttpResponseRedirect(url)
        elif response_type == 301:
            return HttpResponsePermanentRedirect(url)
        else:
            raise Http404('This is not the canonical uri of this object.')


class ThingDetailView(LanguageChangerMixin, CanonicalUrlMixin,
                      AllowPKsTooMixin, TranslatableSlugMixin, AppConfigMixin,
                      DetailView):
    """
    DetailView
    ----------
    This is provided by Django.

    AppConfigMixin
    --------------
    This is provided by Aldryn Apphooks Config and sets the obj properties
    «namespace» and «config» on the obj and passes «current_app» to the
    template context.

    TranslatableSlugMixin
    ---------------------
    This is provided by Django Parler and allows the obj to automatically work
    with translated slugs in a manner that respects «fallbacks»
    and related project settings.

    AppConfigViewUrlMixin
    ---------------------
    This is provided above and overrides Django Parler's «ViewUrlMixin» to
    support application namespaces.

    CanonicalUrlMixin
    -----------------
    This is provided above and automatically handles redirection for
    non-canonical URLs if so configured. This extends AppConfigViewUrlMixin,
    so there's no need to include it if this is used.

    LanguageChangerMixin
    --------------------
    This is defined above and simply provides django CMS language-changer
    support. It is used as a mixin here to keep code DRY if there are multiple
    detail views in the project.
    """
    model = Thing
    view_url_name = 'thing-detail'
    queryset = Thing.objects.published()
    non_canonical_url_response_type = 302


class ThingListView(AppConfigMixin, ListView):
    """
    ListView
    --------
    This is provided by Django.
    """
    model = Thing
    http_method_names = ['get', ]
    queryset = Thing.objects.published()
