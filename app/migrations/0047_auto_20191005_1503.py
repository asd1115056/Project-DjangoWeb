# Generated by Django 2.2.4 on 2019-10-05 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_auto_20191001_1132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet_info',
            name='active_time',
        ),
        migrations.AlterField(
            model_name='pet_info',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]