# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacubes', '0002_ots_ots_clients'),
    ]

    operations = [
        migrations.CreateModel(
            name='carrier',
            fields=[
                ('idcarrier', models.AutoField(serialize=False, primary_key=True)),
                ('codcarrier', models.CharField(max_length=3)),
                ('carriername', models.CharField(max_length=50)),
            ],
        ),
    ]
