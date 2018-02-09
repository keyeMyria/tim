# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-08 11:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelstest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parentchild',
            name='child',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='modelstest.Child'),
        ),
        migrations.AlterField(
            model_name='parentchild',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='modelstest.Parent'),
        ),
    ]