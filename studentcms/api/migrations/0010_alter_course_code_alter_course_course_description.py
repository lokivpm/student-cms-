# Generated by Django 4.2.6 on 2023-11-09 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_course_remove_coursecreation_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_description',
            field=models.TextField(),
        ),
    ]