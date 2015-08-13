# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, resolve, NoReverseMatch

from ..models import Thing
from ..views import ThingDetailView

from . import ThingsTransactionTestCase


class TempProperty(object):
    """
    Simple context manager for setting/restoring properties to temporary values.
    """
    def __init__(self, obj, prop, value):
        self.obj = obj
        self.prop = prop
        self.old_value = getattr(self.obj, prop, None)
        self.value = value

    def __enter__(self):
        setattr(self.obj, self.prop, self.value)
        return self

    def __exit__(self, type, value, traceback):
        setattr(self.obj, self.prop, self.old_value)


class TestViews(ThingsTransactionTestCase):

    def create_thing(self, **kwargs):
        opts = {
            'name': self.rand_str(),
            'app_config': self.app_config,
            'is_published': True
        }
        opts.update(**kwargs)
        return Thing.objects.create(**opts)

    def test_thing_list(self):
        namespace = self.app_config.namespace
        things = [self.create_thing() for _ in range(0, 10)]
        unpublished_thing = things[0]
        unpublished_thing.is_published = False
        unpublished_thing.save()

        response = self.client.get(
            reverse('{0}:thing-list'.format(namespace)))
        for thing in things[1:]:
            self.assertContains(response, thing.name)
        self.assertNotContains(response, unpublished_thing.name)

    def test_thing_detail(self):
        """ Test normal thing detail obj """
        response = self.client.get(self.thing1.get_absolute_url('en'))
        self.thing1.set_current_language('en')
        self.assertContains(response, self.thing1.name)

    def test_thing_detail_wrong_language_handling(self):
        """
        Tests that an attempt to access an object with a mis-matched slug and
        language segment, results in redirection to the correct URL with the
        language-appropriate slug.
        """
        canonical_url = self.thing1.get_absolute_url('en')
        wrong_url = canonical_url.replace('/en/', '/fr/')
        new_url = self.thing1.get_absolute_url('fr')
        response = self.client.get(wrong_url)
        self.assertEquals(response.status_code, 301)
        self.assertTrue(new_url in response.url)

    def test_thing_detail_non_canonical_url_handling(self):
        """
        Tests that attempting to access a thing at a non-canonical url results
        in a redirect when redirect_on_fallback is configured.
        """
        canonical_url = self.thing1.get_absolute_url('en')

        # We're constructing a working URL, but non-canonical URL by replacing
        # the slug with the thing's PK.
        self.thing1.set_current_language('en')
        wrong_url = canonical_url.replace(
            '/{0}/'.format(self.thing1.slug),
            '/{0}/'.format(self.thing1.pk)
        )

        for status_code in [200, 301, 302, 404]:
            with TempProperty(ThingDetailView,
                              'non_canonical_url_response_type', status_code):
                ThingDetailView.non_canonical_url_response_type = status_code
                response = self.client.get(wrong_url)
                self.assertTrue(response.status_code, status_code)

    def test_canonical_url_mixin_default(self):
        """
        Tests that the non_canonical_url_response_type will default to 302 if
        the propert is left unset
        """
        view = ThingDetailView()
        view.non_canonical_url_response_type = None
        self.assertTrue(view.get_non_canonical_url_response_type(), 302)

    def test_get_view_url(self):
        """ Tests that the view's get_view_url() method works """
        url = self.thing1.get_absolute_url('en')
        request = self.get_request('en', url)
        rmatch = resolve(request.path)
        request.resolver_match = rmatch
        view = ThingDetailView()
        view.request = request
        view.config = self.app_config
        view.namespace = self.app_config.namespace
        view.args = rmatch.args
        view.kwargs = rmatch.kwargs
        view_url = view.get_view_url()
        self.assertEqual(view_url, url)

    def test_get_view_url_no_namespace(self):
        """
        Tests that if we don't have an apphook, get_view_url() will raise a
        NoReverseMatch exception.
        """
        url = self.thing1.get_absolute_url('en')
        request = self.get_request('en', url)
        rmatch = resolve(request.path)
        request.resolver_match = rmatch
        view = ThingDetailView()
        view.request = request
        view.args = rmatch.args
        view.kwargs = rmatch.kwargs
        with self.assertRaises(NoReverseMatch):
            view.get_view_url()

    def test_get_view_url_no_view_url_name(self):
        """
        Tests that we get an ImproperlyConfigured raised if we atttempt to use
        get_view_url_name() without first defining the view_url_name property.
        """
        url = self.thing1.get_absolute_url('en')
        request = self.get_request('en', url)
        rmatch = resolve(request.path)
        request.resolver_match = rmatch
        view = ThingDetailView()
        view.request = request
        view.config = self.app_config
        view.namespace = self.app_config.namespace
        view.args = rmatch.args
        view.kwargs = rmatch.kwargs
        view.view_url_name = None
        with self.assertRaises(ImproperlyConfigured):
            view.get_view_url()
