# Generated by Django 4.2.6 on 2023-11-13 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_staffprofile_staffs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('attendance', models.CharField(max_length=1)),
                ('student', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.student')),
            ],
        ),
    ]