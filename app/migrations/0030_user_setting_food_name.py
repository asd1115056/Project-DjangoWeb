# Generated by Django 2.2.3 on 2019-08-23 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20190824_0508'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_setting',
            name='food_Name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.food_type'),
            preserve_default=False,
        ),
    ]