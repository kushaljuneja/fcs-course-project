# Generated by Django 3.2.8 on 2021-10-23 08:00

from django.db import migrations, models
import seller.models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0005_delete_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='verification_document',
            field=models.FileField(upload_to='verification_documents/'),
        ),
    ]
