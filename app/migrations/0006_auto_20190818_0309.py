# Generated by Django 2.2.4 on 2019-08-17 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20190818_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag_info',
            name='category',
            field=models.SmallIntegerField(blank=True, choices=[('0', 'Null'), ('1', 'Cat'), ('2', 'Dog')], default=0, null=True),
        ),
    ]