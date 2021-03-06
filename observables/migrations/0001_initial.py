# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-05 15:30
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='FileValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FileField(upload_to=b'documents/observables/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='IpValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.GenericIPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name='Observable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('notes', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=250, null=True, unique_for_date=b'created')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('first_seen', models.DateTimeField(blank=True, null=True)),
                ('last_seen', models.DateTimeField(blank=True, null=True)),
                ('expiration_date', models.DateTimeField(blank=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('blacklist', models.BooleanField(default=False)),
                ('malware_eradication', models.BooleanField(default=False)),
                ('vurnerability_management', models.BooleanField(default=False)),
                ('to_ids', models.NullBooleanField(default=None)),
                ('sharing', models.BooleanField(default=True)),
                ('rateing', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='observable_author', to='users.Account')),
                ('kill_chain', models.ManyToManyField(blank=True, related_name='obs_kill_chain', to='common.KillChain')),
            ],
        ),
        migrations.CreateModel(
            name='ObservableType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('description', models.TextField(blank=True, null=True)),
                ('type_class', models.CharField(choices=[(b'ip', b'ip_type'), (b'string', b'string_type'), (b'email', b'email_type'), (b'file', b'file_type')], default=b'string', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ObservableValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_value', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='email', to='observables.EmailValue')),
            ],
        ),
        migrations.CreateModel(
            name='StringValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='observablevalue',
            name='file_value',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='file', to='observables.StringValue'),
        ),
        migrations.AddField(
            model_name='observablevalue',
            name='ip_value',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ip', to='observables.IpValue'),
        ),
        migrations.AddField(
            model_name='observablevalue',
            name='obs_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='obs_types', to='observables.ObservableType'),
        ),
        migrations.AddField(
            model_name='observablevalue',
            name='observable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='types_obs', to='observables.Observable'),
        ),
        migrations.AddField(
            model_name='observablevalue',
            name='string_value',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='string', to='observables.StringValue'),
        ),
    ]
