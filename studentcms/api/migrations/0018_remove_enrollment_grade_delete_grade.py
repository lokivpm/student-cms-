# Generated by Django 4.2.6 on 2023-11-11 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_grade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrollment',
            name='grade',
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
    ]
