# Generated by Django 3.2.8 on 2021-10-11 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20211011_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='author',
        ),
    ]
