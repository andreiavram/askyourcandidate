# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-14 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20180414_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='approval_status',
            field=models.SmallIntegerField(choices=[(0, 'In asteptare'), (1, 'Aprobata'), (2, 'Respinsa')], default=0),
        ),
        migrations.AlterUniqueTogether(
            name='candidateanswer',
            unique_together=set([('candidate', 'question')]),
        ),
    ]