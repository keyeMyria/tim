# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-15 17:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0050_auto_20180215_1752'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ipvalue',
            old_name='obs_type',
            new_name='type',
        ),
    ]
