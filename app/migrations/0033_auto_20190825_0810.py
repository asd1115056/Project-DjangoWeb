# Generated by Django 2.2.3 on 2019-08-25 00:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_food_type_created_at'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='user_setting',
            new_name='Schedule',
        ),
    ]
