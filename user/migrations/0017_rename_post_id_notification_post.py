# Generated by Django 5.0.6 on 2024-07-02 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_notification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='post_id',
            new_name='post',
        ),
    ]
