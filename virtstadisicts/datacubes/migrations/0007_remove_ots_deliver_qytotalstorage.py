# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacubes', '0006_auto_20170201_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ots_deliver',
            name='qytotalstorage',
        ),
    ]
