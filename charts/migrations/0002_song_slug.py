# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(populate_from=b'name', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
