# Generated by Django 5.0.7 on 2024-09-14 20:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0012_remove_comment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='rooms.comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]