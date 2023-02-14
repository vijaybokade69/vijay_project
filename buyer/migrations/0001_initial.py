# Generated by Django 4.1.5 on 2023-01-16 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_name', models.CharField(max_length=50)),
                ('Last_name', models.CharField(max_length=70)),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('Password', models.CharField(max_length=15)),
                ('Address', models.TextField(max_length=500)),
            ],
        ),
    ]
