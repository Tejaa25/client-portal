# Generated by Django 4.1.7 on 2023-05-11 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_alter_task_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='role',
        ),
    ]