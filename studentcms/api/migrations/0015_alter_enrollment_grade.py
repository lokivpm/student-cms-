# Generated by Django 4.2.6 on 2023-11-11 03:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_delete_customuser_enrollment_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='grade',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]
