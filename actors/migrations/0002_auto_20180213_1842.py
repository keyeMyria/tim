# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-13 18:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Constituent',
            new_name='Organization',
        ),
        migrations.RemoveField(
            model_name='reporter',
            name='author',
        ),
        migrations.RemoveField(
            model_name='reporter',
            name='type',
        ),
        migrations.DeleteModel(
            name='Reporter',
        ),
    ]