# Generated by Django 2.2.7 on 2019-11-18 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20191117_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='description',
            field=models.CharField(default='', max_length=10000),
        ),
    ]
