# Generated by Django 4.1.7 on 2023-05-05 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_customuser_email_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('PM', 'project manager'), ('FD', 'frontend developer'), ('BD', 'backend developer'), ('UD', 'ui/ux designer'), ('SEO', 'SEO')], default='PM', max_length=3),
        ),
    ]
