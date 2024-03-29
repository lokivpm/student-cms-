# Generated by Django 4.2.6 on 2023-11-08 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_student_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.PositiveIntegerField()),
                ('course_description', models.CharField(max_length=255)),
                ('course_type', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='coursecreation',
            name='category',
        ),
        migrations.RemoveField(
            model_name='coursecreation',
            name='type',
        ),
        migrations.DeleteModel(
            name='CourseCategory',
        ),
        migrations.DeleteModel(
            name='CourseCreation',
        ),
        migrations.DeleteModel(
            name='CourseType',
        ),
    ]
