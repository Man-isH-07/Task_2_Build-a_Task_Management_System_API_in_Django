# Generated by Django 5.1.4 on 2025-01-16 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_alter_task_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='scheduled_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
