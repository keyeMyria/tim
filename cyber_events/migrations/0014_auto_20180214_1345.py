# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-14 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cyber_events', '0013_auto_20180214_1341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='country',
        ),
        migrations.AddField(
            model_name='eventcountry',
            name='event',
            field=models.ManyToManyField(blank=True, related_name='country', to='cyber_events.Event'),
        ),
    ]
