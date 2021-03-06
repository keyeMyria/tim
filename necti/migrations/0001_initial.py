# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-01-26 11:09
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('author', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Account')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='EffectRateing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rateing', models.CharField(max_length=25, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250, unique_for_date=b'created')),
                ('description', models.TextField(blank=True, null=True)),
                ('event_date', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[(b'draft', b'Draft'), (b'published', b'Published')], default=b'draft', max_length=10)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('document', models.FileField(null=True, upload_to=b'documents/events/')),
                ('confidence', models.CharField(choices=[(b'critical', b'critical'), (b'high', b'high'), (b'medium', b'Published'), (b'low', b'low'), (b'unknown', b'unknown')], default=b'unknown', max_length=10)),
                ('risk', models.CharField(choices=[(b'critical', b'critical'), (b'high', b'high'), (b'medium', b'Published'), (b'low', b'low'), (b'unknown', b'unknown')], default=b'unknown', max_length=10)),
                ('tlp', models.CharField(choices=[(b'red', b'red'), (b'amber', b'amber'), (b'green', b'green'), (b'white', b'white')], default=b'red', max_length=10)),
                ('rateing', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('reference', models.CharField(blank=True, max_length=250, null=True)),
                ('author', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Account')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='EventMotive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='motive_ev', to='necti.Event')),
            ],
        ),
        migrations.CreateModel(
            name='EventObservable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='observable_ev', to='necti.Event')),
            ],
        ),
        migrations.CreateModel(
            name='EventReporter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reporter_ev', to='necti.Event')),
            ],
        ),
        migrations.CreateModel(
            name='EventSector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sector_ev', to='necti.Event')),
            ],
        ),
        migrations.CreateModel(
            name='EventThreatActor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='threat_actor_ev', to='necti.Event')),
            ],
        ),
        migrations.CreateModel(
            name='EventTTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ttp_ev', to='necti.Event')),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GeoLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=2, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('rtir_ref_id', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('reporter', models.CharField(choices=[(b'client', b'client')], default=b'client', max_length=10)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Account')),
                ('effect_rateing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inci_eff_rateing', to='necti.EffectRateing')),
            ],
        ),
        migrations.CreateModel(
            name='IncidentFunction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=25, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IncidentValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=25)),
                ('incident', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='incident_value', to='necti.Incident')),
            ],
        ),
        migrations.CreateModel(
            name='Intentsion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KillChain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Motive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
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
                ('author', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Account')),
                ('kill_chain', models.ManyToManyField(blank=True, related_name='obs_kill_chain', to='necti.KillChain')),
            ],
        ),
        migrations.CreateModel(
            name='ObservableType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ObservableValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=25)),
                ('value_md5', models.CharField(editable=False, max_length=255)),
                ('obs_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types', to='necti.ObservableType')),
                ('observable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='types', to='necti.Observable')),
            ],
        ),
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('acronym', models.CharField(max_length=250, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ThreatActor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('first_seen', models.DateTimeField(blank=True, null=True)),
                ('last_seen', models.DateTimeField(blank=True, null=True)),
                ('reference', models.CharField(blank=True, max_length=250, null=True)),
                ('import_name', models.CharField(blank=True, max_length=250, null=True)),
                ('hunting', models.BooleanField(default=False)),
                ('complete', models.BooleanField(default=False)),
                ('document', models.FileField(blank=True, null=True, upload_to=b'documents/threat_actor/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Account')),
                ('motive', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ta_motive', to='necti.Motive')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='ThreatActorAlias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=250, unique=True)),
                ('author', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Account')),
            ],
            options={
                'verbose_name_plural': 'Threat actor aliases',
            },
        ),
        migrations.CreateModel(
            name='ThreatActorAliasCon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taa_alias', to='necti.ThreatActorAlias')),
                ('threat_actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taa_threat_actor', to='necti.ThreatActor')),
            ],
        ),
        migrations.CreateModel(
            name='ThreatActorSources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ta_sources', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ta_sources', to='necti.Subject')),
                ('threat_source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_ta', to='necti.ThreatActor')),
            ],
        ),
        migrations.CreateModel(
            name='ThreatActorType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
                ('reference', models.CharField(blank=True, max_length=250, null=True)),
                ('hunting', models.BooleanField(default=False)),
                ('complete', models.BooleanField(default=False)),
                ('first_seen', models.DateTimeField(blank=True, null=True)),
                ('last_seen', models.DateTimeField(blank=True, null=True)),
                ('author', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Account')),
            ],
            options={
                'verbose_name': 'TTP',
                'verbose_name_plural': 'TTPs',
            },
        ),
        migrations.CreateModel(
            name='TTPCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'TTP Category',
                'verbose_name_plural': 'TTP Categories',
            },
        ),
        migrations.CreateModel(
            name='TTPType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'TTP Type',
                'verbose_name_plural': 'TTP Types',
            },
        ),
        migrations.CreateModel(
            name='EventGeoLocation',
            fields=[
                ('geolocation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='necti.GeoLocation')),
            ],
            bases=('necti.geolocation',),
        ),
        migrations.CreateModel(
            name='TAGeoLocation',
            fields=[
                ('geolocation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='necti.GeoLocation')),
            ],
            bases=('necti.geolocation',),
        ),
        migrations.AddField(
            model_name='ttp',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ttp_category', to='necti.TTPCategory'),
        ),
        migrations.AddField(
            model_name='ttp',
            name='intention',
            field=models.ManyToManyField(blank=True, related_name='ttp_intention', to='necti.Intentsion'),
        ),
        migrations.AddField(
            model_name='ttp',
            name='kill_chain',
            field=models.ManyToManyField(blank=True, related_name='ttp_kill_chain', to='necti.KillChain'),
        ),
        migrations.AddField(
            model_name='ttp',
            name='ttp_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ttp_type', to='necti.TTPType'),
        ),
        migrations.AddField(
            model_name='threatactor',
            name='ta_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ta_type', to='necti.ThreatActorType'),
        ),
        migrations.AddField(
            model_name='subject',
            name='subject_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subject_type', to='necti.SubjectType'),
        ),
        migrations.AddField(
            model_name='incidentvalue',
            name='obs_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inci_obs_types', to='necti.ObservableType'),
        ),
        migrations.AddField(
            model_name='incident',
            name='function',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inci_account', to='necti.IncidentFunction'),
        ),
        migrations.AddField(
            model_name='incident',
            name='impact_rateing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inci_imp_rateing', to='necti.EffectRateing'),
        ),
        migrations.AddField(
            model_name='incident',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inci_owner_account', to='users.Account'),
        ),
        migrations.AddField(
            model_name='eventttp',
            name='ttp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ev_ttp', to='necti.TTP'),
        ),
        migrations.AddField(
            model_name='eventthreatactor',
            name='threat_actor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ev_threat_actor', to='necti.ThreatActor'),
        ),
        migrations.AddField(
            model_name='eventsector',
            name='sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ev_sector', to='necti.Sector'),
        ),
        migrations.AddField(
            model_name='eventreporter',
            name='reporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ev_reporter', to='necti.Reporter'),
        ),
        migrations.AddField(
            model_name='eventobservable',
            name='observable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ev_observable', to='necti.Observable'),
        ),
        migrations.AddField(
            model_name='eventmotive',
            name='motive',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ev_motive', to='necti.Motive'),
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ev_type', to='necti.EventType'),
        ),
        migrations.AddField(
            model_name='event',
            name='tag',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='tageolocation',
            name='ta_geoloc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ta_geoloc', to='necti.ThreatActor'),
        ),
        migrations.AddField(
            model_name='eventgeolocation',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ev_geoloc', to='necti.Event'),
        ),
    ]
