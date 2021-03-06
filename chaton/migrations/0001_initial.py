# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-03 11:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password_hash', models.CharField(blank=True, editable=False, max_length=1024, null=True)),
                ('hash', models.CharField(max_length=64)),
                ('title', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(choices=[('o', 'Owner'), ('r', 'Respondent')], default='r', max_length=1)),
                ('message', models.TextField()),
                ('sent', models.DateTimeField(auto_now_add=True)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chaton.Chat')),
            ],
        ),
    ]
