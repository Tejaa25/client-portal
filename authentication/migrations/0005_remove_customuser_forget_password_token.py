# Generated by Django 4.1.7 on 2023-05-08 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_customuser_forget_password_token_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='forget_password_token',
        ),
    ]
