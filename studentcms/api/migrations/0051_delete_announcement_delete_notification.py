# Generated by Django 4.2.6 on 2023-11-15 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_announcement_notification'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Announcement',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]