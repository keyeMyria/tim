# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-14 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0003_threatactorttp'),
        ('cyber_events', '0018_auto_20180214_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='country',
        ),
        migrations.AddField(
            model_name='event',
            name='targeted_organization',
            field=models.ManyToManyField(blank=True, to='actors.Organization'),
        ),
    ]
