# Generated by Django 5.0.6 on 2024-07-01 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_notification_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='post',
        ),
    ]
