# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import ThingDetailView, ThingListView


urlpatterns = patterns(
    '',
    url(r'^$', ThingListView.as_view(), name='thing-list'),

    # NOTE: We are allowing access by slug and pk here.
    url(r'(?P<pk>\d+)/$', ThingDetailView.as_view(), name='thing-detail'),
    url(r'^(?P<slug>\w[-\w]*)/$', ThingDetailView.as_view(),
        name='thing-detail'),
)
