# Generated by Django 2.1.5 on 2020-02-18 13:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0006_auto_20200218_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monument_reviews',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 2, 18, 13, 44, 48, 246542, tzinfo=utc)),
        ),
    ]
