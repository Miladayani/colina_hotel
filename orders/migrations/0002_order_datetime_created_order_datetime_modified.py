# Generated by Django 5.0.7 on 2024-09-05 15:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='datetime_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='datetime_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified'),
        ),
    ]
