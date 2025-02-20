# Generated by Django 5.0.6 on 2024-05-30 09:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('message', models.TextField(blank=True, max_length=20)),
            ],
        ),
    ]
