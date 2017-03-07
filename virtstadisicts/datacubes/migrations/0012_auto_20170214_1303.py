# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacubes', '0011_auto_20170206_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='ots_deliver',
            name='originaldate',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ots_deliver',
            name='delivereddate',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
