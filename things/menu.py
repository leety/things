# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import (
    get_language_from_request,
    ugettext_lazy as _,
)

from cms.menu_bases import CMSAttachMenu
from cms.apphook_pool import apphook_pool
from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from .models import Thing


class ThingsMenu(CMSAttachMenu):
    # This is what will appear in the drop-list in the Advanced Settings on the
    # page. Best practice is to use the form "<app_name>: <Menu name>"
    name = _('Things: Things')

    def get_nodes(self, request):
        nodes = []
        language = get_language_from_request(request, check_path=True)

        # NOTE: It is important that we only get objects that have an active
        # translation, otherwise, object.get_absolute_url() may return
        # NoReverseMatch exceptions that we will have to catch, if we want to
        # prevent errors from appearing on-screen.
        things = (Thing.objects.published()
                               .language(language)
                               .active_translations(language))

        if hasattr(self, 'instance') and self.instance:  # pragma: no cover
            # If self has a property `instance`, then we're using django CMS
            # 3.0.12 or later, which supports using CMSAttachMenus on multiple,
            # apphook'ed pages, each with their own apphook configuration. So,
            # here we modify the queryset to reflect this.
            app = apphook_pool.get_apphook(self.instance.application_urls)
            if app:
                things = things.namespace(self.instance.application_namespace)

        for thing in things:
            # This try/except seems like overkill here, but if this fails for
            # any reason, this **and any further menus, even from other apps**
            # may not get loaded, so we're extra careful.
            try:
                url = thing.get_absolute_url(language=language)
                node = NavigationNode(thing.name, url, thing.pk)
                nodes.append(node)
            except NoReverseMatch:  # pragma: no cover
                pass

        return nodes

menu_pool.register_menu(ThingsMenu)


# Consider, are there other ways of making menus that users might wish to
# choose from?
