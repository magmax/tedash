# Generated by Django 4.2.5 on 2023-09-28 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tedashcore', '0002_report_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report',
            field=models.FileField(upload_to=''),
        ),
    ]
