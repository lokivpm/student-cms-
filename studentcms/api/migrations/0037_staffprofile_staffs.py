# Generated by Django 4.2.6 on 2023-11-13 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_alter_staffprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffprofile',
            name='staffs',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.staffs'),
        ),
    ]
