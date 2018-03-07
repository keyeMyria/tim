# Generated by Django 2.0.2 on 2018-03-06 10:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20180302_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]