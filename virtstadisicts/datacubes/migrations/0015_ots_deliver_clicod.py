# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacubes', '0014_ots_clients_clicod'),
    ]

    operations = [
        migrations.AddField(
            model_name='ots_deliver',
            name='clicod',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
