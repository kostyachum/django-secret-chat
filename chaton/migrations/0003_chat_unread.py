# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-03 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chaton', '0002_auto_20170603_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='unread',
            field=models.BooleanField(default=True),
        ),
    ]
