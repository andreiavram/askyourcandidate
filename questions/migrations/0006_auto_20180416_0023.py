# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-16 00:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_auto_20180415_2143'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidate',
            options={'ordering': ['order']},
        ),
    ]
