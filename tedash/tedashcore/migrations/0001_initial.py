# Generated by Django 4.2.5 on 2023-09-28 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('created', models.DateTimeField()),
                ('tests', models.PositiveIntegerField()),
                ('failures', models.PositiveIntegerField()),
                ('errors', models.PositiveIntegerField()),
                ('skipped', models.PositiveIntegerField()),
                ('assertions', models.PositiveIntegerField()),
                ('time', models.DurationField()),
                ('report', models.TextField()),
            ],
        ),
    ]