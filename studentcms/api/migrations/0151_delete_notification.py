# Generated by Django 4.2.6 on 2024-02-21 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0150_remove_staffs_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
