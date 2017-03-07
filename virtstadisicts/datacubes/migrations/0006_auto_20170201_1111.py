# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacubes', '0005_auto_20170121_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='ots_deliver',
            name='location',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='ots_deliver',
            name='machine',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='ots_deliver',
            name='qytotalstorage',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
        ),
    ]
