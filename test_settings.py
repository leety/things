#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os


HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Zurich',
    'LANGUAGES': (
        ('en', 'English'),
        ('de', 'German'),
        ('fr', 'French'),
    ),
    'INSTALLED_APPS': [
        'aldryn_apphook_reload',
        'aldryn_apphooks_config',
        'aldryn_boilerplates',
        'aldryn_reversion',
        'aldryn_translation_tools',
        'parler',
        'reversion',
    ],
    'TEMPLATE_DIRS': (
        os.path.join(
            os.path.dirname(__file__),
            'things', 'tests', 'templates'), ),
    'STATICFILES_FINDERS': [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        # important! place right before:
        #     django.contrib.staticfiles.finders.AppDirectoriesFinder
        'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ],
    'TEMPLATE_LOADERS': [
        'django.template.loaders.filesystem.Loader',
        # important! place right before:
        #     django.template.loaders.app_directories.Loader
        'aldryn_boilerplates.template_loaders.AppDirectoriesLoader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    ],
    'ALDRYN_BOILERPLATE_NAME': 'bootstrap3',
    # app-specific
    'PARLER_LANGUAGES': {
        1: (
            {'code': 'de', 'fallback': 'en', },
            {'code': 'fr', 'fallback': 'en', },
            {'code': 'en', 'fallback': 'fr', },
        ),
        'default': {
            'hide_untranslated': False,    # PLEASE DO NOT CHANGE THIS
            'redirect_on_fallback': False,  # PLEASE DO NOT CHANGE THIS
        }
    },
    'SITE_ID': 1,
    'CMS_LANGUAGES': {
        1: [
            {
                'code': 'de',
                'name': 'Deutsche',
                'fallbacks': ['en', ]  # FOR TESTING DO NOT ADD 'fr' HERE
            },
            {
                'code': 'fr',
                'name': 'Française',
                'fallbacks': ['en', ]  # FOR TESTING DO NOT ADD 'de' HERE
            },
            {
                'code': 'en',
                'name': 'English',
                'fallbacks': ['de', 'fr', ]
            },
            {
                'code': 'it',
                'name': 'Italiano',
                'fallbacks': ['fr', ]  # FOR TESTING, LEAVE AS ONLY 'fr'
            },
        ],
        'default': {
            'redirect_on_fallback': True,  # PLEASE DO NOT CHANGE THIS
        }
    },
    #
    # NOTE: The following setting `PARLER_ENABLE_CACHING = False` is required
    # for tests to pass.
    #
    # There appears to be a bug in Parler which leaves translations in Parler's
    # cache even after the parent object has been deleted. In production
    # environments, this is unlikely to affect anything, because newly created
    # objects will have new IDs. In testing, new objects are created with IDs
    # that were previously used, which reveals this issue.
    #
    'PARLER_ENABLE_CACHING': False,
    'ALDRYN_SEARCH_DEFAULT_LANGUAGE': 'en',
    'HAYSTACK_CONNECTIONS': {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
        'de': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    },
    'THUMBNAIL_HIGH_RESOLUTION': True,
    'THUMBNAIL_PROCESSORS': (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        # 'easy_thumbnails.processors.scale_and_crop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters',
    ),
}

# This set of MW classes should work for Django 1.6 and 1.7.
MIDDLEWARE_CLASSES_17 = [
    'aldryn_apphook_reload.middleware.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware'
]

HELPER_SETTINGS['MIDDLEWARE_CLASSES'] = MIDDLEWARE_CLASSES_17


def run():
    from djangocms_helper import runner
    runner.cms('things')

if __name__ == "__main__":
    run()
