# Generated by Django 4.2.6 on 2023-12-05 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0094_transcript_evaluation_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcript',
            name='evaluation_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]