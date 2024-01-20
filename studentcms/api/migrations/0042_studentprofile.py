# Generated by Django 4.2.6 on 2023-11-14 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_staffs_mobile_no_staffs_otp_digit_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profilePhoto', models.ImageField(blank=True, null=True, upload_to='profile_photos/')),
                ('registerNumber', models.CharField(max_length=50, unique=True)),
                ('rollNumber', models.CharField(max_length=50, unique=True)),
                ('department', models.CharField(max_length=100)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('dateOfBirth', models.DateField()),
                ('maritalStatus', models.CharField(max_length=100)),
                ('mobileNumber', models.CharField(max_length=100)),
                ('emergencyMobileNumber', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('bloodGroup', models.CharField(max_length=100)),
                ('religion', models.CharField(max_length=100)),
                ('community', models.CharField(max_length=100)),
            ],
        ),
    ]