# Generated by Django 2.2.4 on 2019-09-28 10:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_auto_20190825_0810'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag_info',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]