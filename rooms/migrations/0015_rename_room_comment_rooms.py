# Generated by Django 5.0.7 on 2024-09-15 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0014_rename_body_comment_content_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='room',
            new_name='rooms',
        ),
    ]
