# Generated by Django 2.2.3 on 2019-08-12 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_tag_info_weight'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag_info',
            old_name='name',
            new_name='nickname',
        ),
        migrations.AlterField(
            model_name='tag_info',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
