# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-05 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0005_auto_20180205_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='observablevalue',
            name='value_md5',
            field=models.CharField(editable=False, max_length=255, null=True),
        ),
    ]
