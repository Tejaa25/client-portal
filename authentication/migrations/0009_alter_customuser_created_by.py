# Generated by Django 4.1.7 on 2023-05-09 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_remove_customuser_is_created_by_manager_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='created_by',
            field=models.IntegerField(null=True),
        ),
    ]
