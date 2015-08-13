# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ThingsConfigTranslation'
        db.create_table(u'things_thingsconfig_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('app_title', self.gf('django.db.models.fields.CharField')(default=u'', max_length=234, blank=True)),
            (u'master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['things.ThingsConfig'])),
        ))
        db.send_create_signal(u'things', ['ThingsConfigTranslation'])

        # Adding unique constraint on 'ThingsConfigTranslation', fields ['language_code', u'master']
        db.create_unique(u'things_thingsconfig_translation', ['language_code', u'master_id'])

        # Adding model 'ThingsConfig'
        db.create_table(u'things_thingsconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('namespace', self.gf('django.db.models.fields.CharField')(default=None, unique=True, max_length=100)),
            ('app_data', self.gf('app_data.fields.AppDataField')(default='{}')),
        ))
        db.send_create_signal(u'things', ['ThingsConfig'])

        # Adding model 'ThingTranslation'
        db.create_table(u'things_thing_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default=u'', max_length=255, blank=True)),
            (u'master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['things.Thing'])),
        ))
        db.send_create_signal(u'things', ['ThingTranslation'])

        # Adding unique constraint on 'ThingTranslation', fields ['language_code', 'slug']
        db.create_unique(u'things_thing_translation', ['language_code', 'slug'])

        # Adding unique constraint on 'ThingTranslation', fields ['language_code', u'master']
        db.create_unique(u'things_thing_translation', ['language_code', u'master_id'])

        # Adding model 'Thing'
        db.create_table(u'things_thing', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('app_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['things.ThingsConfig'])),
        ))
        db.send_create_signal(u'things', ['Thing'])


    def backwards(self, orm):
        # Removing unique constraint on 'ThingTranslation', fields ['language_code', u'master']
        db.delete_unique(u'things_thing_translation', ['language_code', u'master_id'])

        # Removing unique constraint on 'ThingTranslation', fields ['language_code', 'slug']
        db.delete_unique(u'things_thing_translation', ['language_code', 'slug'])

        # Removing unique constraint on 'ThingsConfigTranslation', fields ['language_code', u'master']
        db.delete_unique(u'things_thingsconfig_translation', ['language_code', u'master_id'])

        # Deleting model 'ThingsConfigTranslation'
        db.delete_table(u'things_thingsconfig_translation')

        # Deleting model 'ThingsConfig'
        db.delete_table(u'things_thingsconfig')

        # Deleting model 'ThingTranslation'
        db.delete_table(u'things_thing_translation')

        # Deleting model 'Thing'
        db.delete_table(u'things_thing')


    models = {
        u'things.thing': {
            'Meta': {'object_name': 'Thing'},
            'app_config': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['things.ThingsConfig']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'things.thingsconfig': {
            'Meta': {'object_name': 'ThingsConfig'},
            'app_data': ('app_data.fields.AppDataField', [], {'default': "'{}'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'namespace': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'things.thingsconfigtranslation': {
            'Meta': {'unique_together': "[(u'language_code', u'master')]", 'object_name': 'ThingsConfigTranslation', 'db_table': "u'things_thingsconfig_translation'"},
            'app_title': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '234', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            u'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['things.ThingsConfig']"})
        },
        u'things.thingtranslation': {
            'Meta': {'unique_together': "[(u'language_code', u'slug'), (u'language_code', u'master')]", 'object_name': 'ThingTranslation', 'db_table': "u'things_thing_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            u'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['things.Thing']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['things']