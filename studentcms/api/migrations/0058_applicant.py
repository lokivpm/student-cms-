# Generated by Django 4.2.6 on 2023-11-17 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0057_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('desired_major', models.CharField(max_length=20)),
                ('school_name', models.CharField(max_length=30)),
                ('high_school_gpa', models.FloatField()),
                ('aadhaar_number', models.CharField(max_length=15)),
            ],
        ),
    ]
