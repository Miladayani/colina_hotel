# Generated by Django 5.0.7 on 2024-09-14 08:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0009_alter_room_price_per_night'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rooms',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='rooms.room'),
        ),
    ]
