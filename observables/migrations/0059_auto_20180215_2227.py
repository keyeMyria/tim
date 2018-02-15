# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-15 22:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0058_auto_20180215_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipvalue',
            name='value',
            field=models.GenericIPAddressField(blank=True, null=True, unique=True),
        ),
    ]
