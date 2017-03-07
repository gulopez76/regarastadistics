# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacubes', '0007_remove_ots_deliver_qytotalstorage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ots_deliver',
            name='delivereddate',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
