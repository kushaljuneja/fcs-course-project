# Generated by Django 3.2.8 on 2021-11-08 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0023_merge_0022_auto_20211108_0237_0022_auto_20211108_0246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbase',
            name='otp',
            field=models.SmallIntegerField(default=123456),
        ),
    ]
