# Generated by Django 2.2.4 on 2019-09-30 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_auto_20190930_1211'),
    ]

    operations = [
        migrations.RenameField(
            model_name='env_info',
            old_name='name',
            new_name='location_id',
        ),
        migrations.RenameField(
            model_name='env_info',
            old_name='location',
            new_name='location_name',
        ),
    ]