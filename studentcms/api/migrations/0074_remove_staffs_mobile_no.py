# Generated by Django 4.2.6 on 2023-11-19 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0073_staffs_mobile_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staffs',
            name='mobile_no',
        ),
    ]
