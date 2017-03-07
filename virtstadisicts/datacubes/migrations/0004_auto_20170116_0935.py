# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacubes', '0003_carrier'),
    ]

    operations = [
        migrations.AddField(
            model_name='ots_deliver',
            name='delivereddate',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='ots_deliver',
            name='idcarrier',
            field=models.ForeignKey(default=24, to='datacubes.carrier'),
        ),
        migrations.AddField(
            model_name='ots_deliver',
            name='totalstorage',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
        ),
    ]
