# Generated by Django 2.2.4 on 2019-10-17 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20191012_0119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='food_Name',
        ),
        migrations.AlterField(
            model_name='device_info',
            name='device_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
