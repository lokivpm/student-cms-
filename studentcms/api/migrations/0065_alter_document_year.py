# Generated by Django 4.2.6 on 2023-11-17 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0064_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='year',
            field=models.CharField(max_length=20),
        ),
    ]
