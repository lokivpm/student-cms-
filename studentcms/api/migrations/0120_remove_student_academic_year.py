# Generated by Django 4.2.6 on 2024-01-20 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0119_remove_course_academic_year_student_academic_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='academic_year',
        ),
    ]
