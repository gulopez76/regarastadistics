# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacubes', '0010_auto_20170202_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='ots_deliver',
            name='enddate',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ots_deliver',
            name='agent',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ots_deliver',
            name='idcarrier',
            field=models.ForeignKey(default=25, to='datacubes.carrier'),
        ),
    ]
