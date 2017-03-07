# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacubes', '0009_auto_20170202_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='ots_deliver',
            name='agent',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ots_deliver',
            name='location',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
