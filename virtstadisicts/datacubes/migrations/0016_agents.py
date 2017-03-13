# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datacubes', '0015_ots_deliver_clicod'),
    ]

    operations = [
        migrations.CreateModel(
            name='agents',
            fields=[
                ('idagent', models.AutoField(serialize=False, primary_key=True)),
                ('agentcode', models.CharField(max_length=4)),
                ('agentname', models.CharField(max_length=100)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
