# Generated by Django 2.0.2 on 2018-03-07 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0005_auto_20180307_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actor', to='events.Event'),
        ),
    ]