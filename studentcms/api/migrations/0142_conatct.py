# Generated by Django 4.2.6 on 2024-02-14 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0141_delete_flatpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conatct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('query', models.TextField()),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
