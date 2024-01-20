# Generated by Django 4.2.6 on 2023-11-21 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0079_alter_staffstudentchat_msg_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.staffs'),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='api.course'),
        ),
    ]