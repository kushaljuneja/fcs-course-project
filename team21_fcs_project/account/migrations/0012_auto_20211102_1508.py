# Generated by Django 3.2.8 on 2021-11-02 09:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20211024_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbase',
            name='is_admin_request_sent',
        ),
        migrations.RemoveField(
            model_name='userbase',
            name='is_seller',
        ),
        migrations.RemoveField(
            model_name='userbase',
            name='otp_secret',
        ),
        migrations.RemoveField(
            model_name='userbase',
            name='two_fa_enabled',
        ),
        migrations.RemoveField(
            model_name='userbase',
            name='updated',
        ),
        migrations.AlterField(
            model_name='userbase',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='userbase',
            name='name',
            field=models.CharField(blank=True, default=django.utils.timezone.now, max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userbase',
            name='user_name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
