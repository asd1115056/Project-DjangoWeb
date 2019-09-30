# Generated by Django 2.2.4 on 2019-09-28 15:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_tag_info_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag_info',
            name='time',
        ),
        migrations.AddField(
            model_name='pet_info',
            name='active_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]