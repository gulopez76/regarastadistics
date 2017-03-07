# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacubes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ots',
            fields=[
                ('idot', models.AutoField(serialize=False, primary_key=True)),
                ('ot', models.CharField(max_length=7)),
                ('otname', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ots_clients',
            fields=[
                ('idclient', models.AutoField(serialize=False, primary_key=True)),
                ('clientname', models.CharField(max_length=50)),
            ],
        ),
    ]
