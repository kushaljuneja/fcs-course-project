# Generated by Django 3.2.8 on 2021-10-16 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20211016_0036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbase',
            name='about',
        ),
        migrations.AddField(
            model_name='userbase',
            name='otp_secret',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
