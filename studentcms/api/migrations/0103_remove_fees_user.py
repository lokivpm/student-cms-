# Generated by Django 4.2.6 on 2023-12-10 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0102_remove_student_user_alter_payment_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fees',
            name='user',
        ),
    ]