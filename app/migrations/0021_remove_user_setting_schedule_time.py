# Generated by Django 2.2.3 on 2019-08-22 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_user_setting_schedule_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_setting',
            name='schedule_time',
        ),
    ]