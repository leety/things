# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app_data.fields
import aldryn_translation_tools.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_published', models.BooleanField(default=False, verbose_name='is published?')),
            ],
            options={
                'verbose_name': 'thing',
                'verbose_name_plural': 'things',
            },
            bases=(aldryn_translation_tools.models.TranslatedAutoSlugifyMixin, aldryn_translation_tools.models.TranslationHelperMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ThingsConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, verbose_name='type')),
                ('namespace', models.CharField(default=None, unique=True, max_length=100, verbose_name='instance namespace')),
                ('app_data', app_data.fields.AppDataField(default=b'{}', editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ThingsConfigTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('app_title', models.CharField(default='', max_length=234, verbose_name='application title', blank=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='things.ThingsConfig', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'things_thingsconfig_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'things config Translation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ThingTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('name', models.CharField(default='', max_length=255, verbose_name='name')),
                ('slug', models.SlugField(default='', max_length=255, verbose_name='slug', blank=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='things.Thing', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'things_thing_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'thing Translation',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='thingtranslation',
            unique_together=set([('language_code', 'master'), ('language_code', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='thingsconfigtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AddField(
            model_name='thing',
            name='app_config',
            field=models.ForeignKey(verbose_name='app_config', to='things.ThingsConfig'),
            preserve_default=True,
        ),
    ]
