# Generated by Django 4.2.6 on 2023-11-12 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_alter_staffprofile_staffcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffprofile',
            name='email',
            field=models.CharField(editable=False, max_length=100),
        ),
    ]