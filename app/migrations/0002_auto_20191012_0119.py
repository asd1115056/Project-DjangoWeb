# Generated by Django 2.2.4 on 2019-10-11 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_info',
            name='device_name',
            field=models.CharField(blank=True, default='null', max_length=100, null=True),
        ),
    ]
