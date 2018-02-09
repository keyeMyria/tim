# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-08 12:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0017_auto_20180208_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ipvalueselect',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='ipvalueselect',
            name='value',
        ),
        migrations.AddField(
            model_name='observablevalue',
            name='value',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='observable_value', to='observables.IpValue'),
        ),
        migrations.DeleteModel(
            name='IpValueSelect',
        ),
    ]