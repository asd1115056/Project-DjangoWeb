# Generated by Django 2.2.3 on 2019-08-24 09:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20190824_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='food_type',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]