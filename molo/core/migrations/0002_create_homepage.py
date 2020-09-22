# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_homepage(apps, schema_editor):
    # Get models
    Page = apps.get_model('wagtailcore.Page')
    apps.get_model('wagtailcore.Site')

    # Delete the default homepage
    Page.objects.get(id=2).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_homepage),
    ]
