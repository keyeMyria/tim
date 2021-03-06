# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-08 12:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0016_auto_20180208_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipvalueselect',
            name='ip',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ip_value', to='observables.ObservableValue'),
        ),
        migrations.AlterField(
            model_name='ipvalueselect',
            name='value',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='observable_value', to='observables.IpValue'),
        ),
        migrations.AlterField(
            model_name='observablevalue',
            name='obs_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observable', to='observables.ObservableType'),
        ),
        migrations.AlterField(
            model_name='observablevalue',
            name='observable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obs_type', to='observables.Observable'),
        ),
    ]
