# Generated by Django 4.2.6 on 2023-11-16 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0056_delete_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('receiver_staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages_staff', to='api.staffs')),
                ('receiver_student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages_student', to='api.student')),
                ('sender_staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages_staff', to='api.staffs')),
                ('sender_student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages_student', to='api.student')),
            ],
        ),
    ]
