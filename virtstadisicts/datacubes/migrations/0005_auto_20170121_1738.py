# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacubes', '0004_auto_20170116_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ots_deliver',
            name='totalstorage',
            field=models.IntegerField(default=0),
        ),
    ]
