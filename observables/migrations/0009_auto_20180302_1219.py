# Generated by Django 2.0.2 on 2018-03-02 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0008_auto_20180302_1209'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='observablevalue',
            unique_together={('observable', 'string'), ('email', 'string'), ('ip', 'string'), ('observable', 'email'), ('email', 'ip'), ('observable', 'ip'), ('ip', 'email')},
        ),
    ]