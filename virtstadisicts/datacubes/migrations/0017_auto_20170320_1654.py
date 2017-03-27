# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacubes', '0016_agents'),
    ]

    operations = [
        migrations.CreateModel(
            name='agentrights',
            fields=[
                ('idagentrights', models.AutoField(serialize=False, primary_key=True)),
                ('idagent', models.ForeignKey(to='datacubes.agents')),
            ],
        ),
        migrations.CreateModel(
            name='agentsgroups',
            fields=[
                ('idagentgroup', models.AutoField(serialize=False, primary_key=True)),
                ('groupagentcode', models.CharField(max_length=3, blank=True)),
                ('groupagentdesc', models.CharField(max_length=50, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='agentrights',
            name='idagentgroup',
            field=models.ForeignKey(to='datacubes.agentsgroups'),
        ),
    ]
