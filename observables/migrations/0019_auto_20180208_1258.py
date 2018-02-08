# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-08 12:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0018_auto_20180208_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='observablevalue',
            name='value',
        ),
        migrations.AddField(
            model_name='observablevalue',
            name='ip_value',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ip_value', to='observables.IpValue'),
        ),
    ]
