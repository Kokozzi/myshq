# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-14 06:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0007_sdn_device_last_polled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sdn_device',
            name='last_polled',
            field=models.DateTimeField(),
        ),
    ]