# Generated by Django 4.2.6 on 2023-11-06 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_staffs_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffs',
            old_name='name',
            new_name='full_name',
        ),
    ]
