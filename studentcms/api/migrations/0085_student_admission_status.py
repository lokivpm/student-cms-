# Generated by Django 4.2.6 on 2023-12-01 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0084_remove_student_admission_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='admission_status',
            field=models.BooleanField(default=False),
        ),
    ]
