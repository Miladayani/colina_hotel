# Generated by Django 5.0.7 on 2024-09-08 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0008_alter_room_price_per_night'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='price_per_night',
            field=models.IntegerField(),
        ),
    ]