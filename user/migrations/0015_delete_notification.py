# Generated by Django 5.0.6 on 2024-07-02 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_notification_post_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
