# Generated by Django 4.2.6 on 2023-12-04 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0093_alter_attendance_attendance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcript',
            name='evaluation_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='transcript',
            name='transcript_file',
            field=models.FileField(blank=True, null=True, upload_to='transcripts/'),
        ),
    ]
