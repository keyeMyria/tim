# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-14 13:50
from __future__ import unicode_literals

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cyber_events', '0016_remove_event_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=746, multiple=True),
        ),
    ]
