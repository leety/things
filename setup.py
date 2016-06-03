# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from things import __version__

REQUIREMENTS = [
    'Django>=1.6,<1.10',
    'aldryn-apphooks-config>=0.2.4',
    'aldryn-boilerplates>=0.6.0',
    'aldryn-common>=0.1.3',
    'aldryn-reversion>=0.1.0',
    'aldryn-translation-tools>=0.1.1',
    'django-parler>=1.4',
    'django-reversion>=1.8.2,<1.11',
]

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 1.6',
    'Framework :: Django :: 1.7',
    'Framework :: Django :: 1.8',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='things',
    version=__version__,
    description='A starter project for your translatable, revision-able, '
                'Spaces-supporting Aldryn addon',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/things',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    long_description=open('README.rst').read(),
    include_package_data=True,
    zip_safe=False,
    test_suite="test_settings.run",
)
