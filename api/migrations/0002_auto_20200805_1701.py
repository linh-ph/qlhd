# Generated by Django 3.0.7 on 2020-08-05 17:01

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='url',
        ),
        migrations.AddField(
            model_name='distributor',
            name='url',
            field=models.ImageField(default=2, upload_to=api.models.upload_path),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='infoimage',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]