# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-15 17:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0046_auto_20180215_1332'),
    ]

    operations = [
        migrations.RenameField(
            model_name='observablevalues',
            old_name='value',
            new_name='ip',
        ),
    ]
