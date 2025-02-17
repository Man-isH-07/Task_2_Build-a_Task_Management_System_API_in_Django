# Generated by Django 5.1.4 on 2025-01-20 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0007_task_email_alter_task_scheduled_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='email',
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Ongoing', 'Ongoing'), ('Completed', 'Completed'), ('Pending', 'Pending')], default='Ongoing', max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('Personal', 'Personal'), ('Work', 'Work'), ('Other', 'Other')], default='Other', max_length=50),
        ),
    ]
