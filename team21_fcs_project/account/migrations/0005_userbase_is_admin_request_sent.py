# Generated by Django 3.2.8 on 2021-10-14 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20211014_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbase',
            name='is_admin_request_sent',
            field=models.BooleanField(default=False),
        ),
    ]