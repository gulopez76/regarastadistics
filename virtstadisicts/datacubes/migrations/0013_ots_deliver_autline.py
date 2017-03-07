# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacubes', '0012_auto_20170214_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='ots_deliver',
            name='autline',
            field=models.BigIntegerField(default=0),
        ),
    ]
