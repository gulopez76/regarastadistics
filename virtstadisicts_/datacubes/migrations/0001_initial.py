# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='ots_deliver',
            fields=[
                ('iddeliver', models.AutoField(serialize=False, primary_key=True)),
                ('sentdate', models.DateField(auto_now_add=True)),
                ('ot', models.CharField(max_length=7)),
                ('clientname', models.CharField(max_length=50)),
                ('otname', models.CharField(max_length=50)),
                ('codproduct', models.CharField(max_length=25)),
                ('clientcommand', models.CharField(max_length=30)),
                ('deliverparcial', models.DecimalField(max_digits=10, decimal_places=2)),
                ('totaldeliver', models.DecimalField(max_digits=10, decimal_places=2)),
                ('nominalprovided', models.DecimalField(max_digits=10, decimal_places=2)),
                ('totalstorage', models.IntegerField(default=0)),
                ('delivereddate', models.DateTimeField(auto_now_add=True, null=True)),
                ('machine', models.CharField(max_length=25, null=True)),
                ('location', models.CharField(max_length=30, null=True)),
                ('agent', models.IntegerField(default=0)),
                ('enddate', models.DateTimeField(null=True, blank=True)),
                ('originaldate', models.DateTimeField(null=True, blank=True)),
                ('autline', models.BigIntegerField(default=0)),
                ('idcarrier', models.ForeignKey(default=25, to='datacubes.carrier')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='userprofile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(null=True, upload_to=b'photos/', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
