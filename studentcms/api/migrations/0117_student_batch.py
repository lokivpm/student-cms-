# Generated by Django 4.2.6 on 2024-01-05 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0116_rename_acadamic_year_course_academic_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='batch',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
