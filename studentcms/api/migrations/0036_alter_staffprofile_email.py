# Generated by Django 4.2.6 on 2023-11-12 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_alter_staffprofile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffprofile',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]