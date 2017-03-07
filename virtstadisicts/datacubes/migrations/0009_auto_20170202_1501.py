# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacubes', '0008_auto_20170201_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ots_deliver',
            name='location',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
