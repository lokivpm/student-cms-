# Generated by Django 4.2.6 on 2024-02-03 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0127_student_confirm_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='full_name',
        ),
    ]
