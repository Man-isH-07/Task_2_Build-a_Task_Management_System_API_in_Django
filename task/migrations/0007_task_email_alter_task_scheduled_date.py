# Generated by Django 5.1.4 on 2025-01-20 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_task_scheduled_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='scheduled_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
