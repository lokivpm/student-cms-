# Generated by Django 4.2.6 on 2023-11-06 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_name_staffs_full_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('course_description', models.TextField()),
            ],
            options={
                'verbose_name_plural': '2.Course Category',
            },
        ),
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('course_description', models.TextField()),
            ],
            options={
                'verbose_name_plural': '1.Course Type',
            },
        ),
    ]
