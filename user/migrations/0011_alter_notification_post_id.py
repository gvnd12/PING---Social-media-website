# Generated by Django 5.0.6 on 2024-07-02 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_notification_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='post_id',
            field=models.IntegerField(default=False),
        ),
    ]
