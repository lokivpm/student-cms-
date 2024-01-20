# Generated by Django 4.2.6 on 2023-11-11 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_transcript'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profilePhoto', models.ImageField(blank=True, null=True, upload_to='profile_photos/')),
                ('staffCode', models.CharField(max_length=50)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('staffType', models.CharField(max_length=100)),
                ('staffRoll', models.CharField(max_length=100)),
                ('dateOfJoining', models.DateField()),
                ('gender', models.CharField(max_length=100)),
                ('dateOfBirth', models.DateField()),
                ('maritalStatus', models.CharField(max_length=100)),
                ('bloodGroup', models.CharField(max_length=100)),
                ('religion', models.CharField(max_length=100)),
                ('community', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('mobileNumber', models.CharField(max_length=100)),
                ('emergencyMobileNumber', models.CharField(max_length=100)),
            ],
        ),
    ]