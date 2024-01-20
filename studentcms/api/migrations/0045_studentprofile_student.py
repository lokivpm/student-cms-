# Generated by Django 4.2.6 on 2023-11-14 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_remove_student_otp_digit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='student',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='api.student'),
        ),
    ]
