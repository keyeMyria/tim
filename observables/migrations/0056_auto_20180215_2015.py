# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-15 20:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0055_auto_20180215_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observablevalues',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='observable_value', to='observables.ObservableType'),
        ),
    ]
