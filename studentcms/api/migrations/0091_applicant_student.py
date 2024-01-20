# Generated by Django 4.2.6 on 2023-12-01 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0090_remove_applicant_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='api.student'),
        ),
    ]