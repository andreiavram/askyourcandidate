# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-14 23:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20180414_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='motivation',
            field=models.TextField(default='motivation'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='candidateanswer',
            name='text',
            field=models.TextField(verbose_name='Raspunsul tau'),
        ),
    ]
