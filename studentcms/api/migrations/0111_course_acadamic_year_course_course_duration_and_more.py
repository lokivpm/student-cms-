# Generated by Django 4.2.6 on 2023-12-30 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0110_remove_document_date_of_join_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='acadamic_year',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='course_duration',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_ponits',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]